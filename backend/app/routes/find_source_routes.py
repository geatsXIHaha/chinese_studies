"""Chinese quote/source finder API routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ChineseQuote
from app.schemas import FindSourceRequest, FindSourceResponse, FindSourceSuggestionsResponse
from app.services import ai_service

router = APIRouter(prefix="/api", tags=["quotes"])


@router.post("/find-source", response_model=FindSourceSuggestionsResponse)
def find_source(request: FindSourceRequest, db: Session = Depends(get_db)):
    text = (request.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    matches = (
        db.query(ChineseQuote)
        .filter(
            (ChineseQuote.quote.ilike(f"%{text}%"))
            | (ChineseQuote.source.ilike(f"%{text}%"))
            | (ChineseQuote.author.ilike(f"%{text}%"))
            | (ChineseQuote.meaning.ilike(f"%{text}%"))
        )
        .limit(5)
        .all()
    )

    results = []
    is_partial = len(text) < 8
    if not matches or is_partial:
        try:
            ai_results = ai_service.find_chinese_quotes_ai(text)
        except ValueError:
            raise HTTPException(status_code=502, detail="AI search unavailable")

        results = [
            FindSourceResponse(
                original_text=item.get("original_text", ""),
                source=item.get("source", ""),
                author=item.get("author"),
                context_explanation=item.get("context_explanation"),
            )
            for item in ai_results
        ]
    if not results and matches:
        results = [
            FindSourceResponse(
                original_text=quote.quote,
                source=quote.source,
                author=quote.author,
                context_explanation=quote.meaning,
            )
            for quote in matches
        ]

    suggestions = []
    try:
        suggestions = ai_service.suggest_chinese_quotes(text, request.max_suggestions)
    except ValueError:
        suggestions = []

    return FindSourceSuggestionsResponse(results=results, suggestions=suggestions)