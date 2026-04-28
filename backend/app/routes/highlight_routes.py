"""Highlight and annotation API routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import (
    HighlightCreate,
    HighlightResponse,
    TextExplanationRequest,
    TextExplanationResponse,
    TranslateRequest,
    TranslateResponse,
)
from app.services import HighlightService, ai_service

router = APIRouter(prefix="/api/highlights", tags=["highlights"])


@router.post("/", response_model=HighlightResponse)
def create_highlight(highlight: HighlightCreate, db: Session = Depends(get_db)):
    """Create a new highlight"""
    return HighlightService.create_highlight(db, highlight)


@router.get("/paper/{paper_id}", response_model=List[HighlightResponse])
def get_highlights_for_paper(
    paper_id: int,
    user_id: str = Query(...),
    db: Session = Depends(get_db),
):
    """Get all highlights for a paper"""
    return HighlightService.get_highlights_for_paper(db, paper_id, user_id)


@router.delete("/{highlight_id}")
def delete_highlight(highlight_id: int, db: Session = Depends(get_db)):
    """Delete a highlight"""
    if not HighlightService.delete_highlight(db, highlight_id):
        raise HTTPException(status_code=404, detail="Highlight not found")
    return {"message": "Highlight deleted successfully"}


@router.post("/explain", response_model=TextExplanationResponse)
def explain_text(request: TextExplanationRequest):
    """Get AI explanation for highlighted text"""
    result = ai_service.explain_text(request.text, request.context)
    return TextExplanationResponse(
        original_text=result["original_text"],
        explanation=result["explanation"],
        key_terms=result["key_terms"],
    )


@router.post("/translate", response_model=TranslateResponse)
def translate_text(request: TranslateRequest):
    """Translate selected text"""
    translated = ai_service.translate_text(request.text, request.target_language)
    return TranslateResponse(
        original_text=request.text,
        translated_text=translated,
    )


@router.post("/{highlight_id}/explanation")
def add_explanation_to_highlight(
    highlight_id: int,
    request: TextExplanationRequest,
    db: Session = Depends(get_db),
):
    """Generate and save explanation for a highlight"""
    result = ai_service.explain_text(request.text, request.context)
    updated = HighlightService.update_highlight_explanation(
        db, highlight_id, result["explanation"]
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Highlight not found")
    return {
        "highlight_id": highlight_id,
        "explanation": result["explanation"],
        "key_terms": result["key_terms"],
    }
