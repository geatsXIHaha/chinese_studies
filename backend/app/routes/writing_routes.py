"""Essay and writing assistance API routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import (
    EssayIdeaCreate,
    EssayIdeaResponse,
    WriteHumaniserRequest,
    WriteHumaniserResponse,
    PdfChatRequest,
    PdfChatResponse,
)
from app.services import EssayIdeaService, ai_service, PaperService

router = APIRouter(prefix="/api/writing", tags=["writing"])


@router.post("/essay-ideas/{paper_id}")
def generate_essay_ideas(
    paper_id: int,
    user_id: str = Query(...),
    db: Session = Depends(get_db),
):
    """Generate essay ideas for a paper"""
    paper = PaperService.get_paper(db, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    ideas = ai_service.generate_essay_ideas(paper.title, paper.abstract)

    # Save ideas to database
    saved_ideas = []
    for idea_text in ideas:
        idea = EssayIdeaCreate(
            paper_id=paper_id,
            user_id=user_id,
            idea=idea_text,
            keywords=paper.keywords or "",
        )
        saved_idea = EssayIdeaService.create_essay_idea(db, idea)
        saved_ideas.append(saved_idea)

    return {
        "paper_id": paper_id,
        "ideas": [{"id": idea.id, "idea": idea.idea} for idea in saved_ideas],
    }


@router.get("/essay-ideas/{paper_id}", response_model=List[EssayIdeaResponse])
def get_essay_ideas(
    paper_id: int,
    user_id: str = Query(...),
    db: Session = Depends(get_db),
):
    """Get essay ideas for a paper"""
    return EssayIdeaService.get_essay_ideas_for_paper(db, paper_id, user_id)


@router.delete("/essay-ideas/{idea_id}")
def delete_essay_idea(idea_id: int, db: Session = Depends(get_db)):
    """Delete an essay idea"""
    if not EssayIdeaService.delete_essay_idea(db, idea_id):
        raise HTTPException(status_code=404, detail="Essay idea not found")
    return {"message": "Essay idea deleted successfully"}


@router.post("/humanise", response_model=WriteHumaniserResponse)
def humanise_text(request: WriteHumaniserRequest):
    """Make academic writing more natural and readable"""
    humanised = ai_service.humanise_writing(request.text)
    return WriteHumaniserResponse(
        original_text=request.text,
        humanised_text=humanised,
    )


@router.post("/pdf-chat", response_model=PdfChatResponse)
def pdf_chat(request: PdfChatRequest, db: Session = Depends(get_db)):
    """Answer questions based on PDF content"""
    question = (request.message or "").strip()
    if not question:
        raise HTTPException(status_code=400, detail="Message is required")

    paper = PaperService.get_paper(db, request.paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    context = paper.full_text or paper.abstract or ""
    reply = ai_service.answer_pdf_question(question, context)
    return PdfChatResponse(reply=reply)
