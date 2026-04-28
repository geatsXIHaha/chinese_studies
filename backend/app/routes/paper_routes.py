"""Paper API routes"""
import os
import re
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from pypdf import PdfReader

from app.database import get_db
from app.schemas import PaperCreate, PaperResponse
from app.services import PaperService, ai_service

router = APIRouter(prefix="/api/papers", tags=["papers"])

UPLOAD_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
)


def _clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def _extract_year(text: str) -> int | None:
    match = re.search(r"(19\d{2}|20\d{2})", text)
    return int(match.group(1)) if match else None


def _extract_title(text: str) -> str | None:
    for line in text.splitlines():
        line = _clean_text(line)
        if len(line) >= 5 and re.search(r"[\u4e00-\u9fff]", line):
            return line
    return None


def _extract_author(text: str) -> str | None:
    match = re.search(r"(?:作者|Author)\s*[:：]\s*(.+)", text)
    if match:
        return _clean_text(match.group(1)).split(" ")[0]
    return None


def _extract_abstract(text: str) -> str | None:
    match = re.search(r"摘要\s*[:：]\s*(.{20,1200})", text, re.S)
    if match:
        return _clean_text(match.group(1))[:800]
    return None


def _extract_pdf_fields(file_path: str) -> dict:
    reader = PdfReader(file_path)
    metadata = reader.metadata or {}

    first_page_text = ""
    if reader.pages:
        first_page_text = reader.pages[0].extract_text() or ""

    combined_text = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text:
            combined_text.append(page_text)

    combined_text_str = "\n".join(combined_text)
    cleaned_first_page = _clean_text(first_page_text)

    ai_result = ai_service.extract_pdf_metadata(combined_text_str)

    title = (
        ai_result.get("title")
        or metadata.get("/Title")
        or _extract_title(first_page_text)
    )
    author = (
        ai_result.get("author")
        or metadata.get("/Author")
        or _extract_author(first_page_text)
    )
    abstract = ai_result.get("abstract") or _extract_abstract(combined_text_str)

    year_source = ai_result.get("year") or metadata.get("/CreationDate") or combined_text_str
    year = _extract_year(str(year_source))

    full_text = combined_text_str.replace("\r\n", "\n").strip()
    if len(full_text) > 200000:
        full_text = full_text[:200000]

    return {
        "title": _clean_text(title) if title else "未识别标题",
        "authors": _clean_text(author) if author else "未知作者",
        "abstract": abstract or "未识别摘要",
        "full_text": full_text or "未能提取 PDF 文本内容",
        "year": year,
        "first_page_text": cleaned_first_page,
    }


@router.get("/", response_model=List[PaperResponse])
def list_papers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all papers with pagination"""
    return PaperService.list_papers(db, skip, limit)


@router.get("/search/{query}", response_model=List[PaperResponse])
def search_papers(
    query: str,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Search papers by title, authors, or keywords"""
    if not query:
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    return PaperService.search_papers(db, query, limit)


@router.get("/search", response_model=List[PaperResponse])
def search_papers_query(
    query: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Search papers by title, authors, or keywords (query param)"""
    return PaperService.search_papers(db, query, limit)


@router.post("/", response_model=PaperResponse)
def create_paper(paper: PaperCreate, db: Session = Depends(get_db)):
    """Create a new paper"""
    return PaperService.create_paper(db, paper)


@router.get("/{paper_id}", response_model=PaperResponse)
def get_paper(paper_id: int, db: Session = Depends(get_db)):
    """Get a paper by ID"""
    paper = PaperService.get_paper(db, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper


@router.delete("/{paper_id}")
def delete_paper(paper_id: int, db: Session = Depends(get_db)):
    """Delete a paper"""
    if not PaperService.delete_paper(db, paper_id):
        raise HTTPException(status_code=404, detail="Paper not found")
    return {"message": "Paper deleted successfully"}


@router.post("/upload", response_model=PaperResponse)
def upload_paper_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a PDF and create a placeholder paper entry"""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    safe_name = f"{uuid.uuid4().hex}_{os.path.basename(file.filename)}"
    save_path = os.path.join(UPLOAD_DIR, safe_name)

    with open(save_path, "wb") as out_file:
        out_file.write(file.file.read())

    extracted = _extract_pdf_fields(save_path)
    publication_date = (
        datetime(extracted["year"], 1, 1) if extracted["year"] else datetime.utcnow()
    )

    paper = PaperCreate(
        title=extracted["title"],
        authors=extracted["authors"],
        abstract=extracted["abstract"],
        full_text=extracted["full_text"],
        publication_date=publication_date,
        source_url=f"/uploads/{safe_name}",
        keywords="上传, PDF",
    )

    return PaperService.create_paper(db, paper)
