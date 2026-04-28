"""Chinese quotes and cultural reference API routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import ChineseQuote
from app.schemas import ChineseQuoteCreate, ChineseQuoteResponse
from app.services import ai_service

router = APIRouter(prefix="/api/quotes", tags=["quotes"])


@router.get("/search", response_model=List[ChineseQuoteResponse])
def search_quotes(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    """Search for Chinese quotes related to keyword (名句溯源)"""
    # First try database
    quotes = (
        db.query(ChineseQuote)
        .filter(
            (ChineseQuote.quote.ilike(f"%{keyword}%"))
            | (ChineseQuote.source.ilike(f"%{keyword}%"))
            | (ChineseQuote.author.ilike(f"%{keyword}%"))
            | (ChineseQuote.meaning.ilike(f"%{keyword}%"))
        )
        .limit(5)
        .all()
    )

    # If no results, use AI service to find related quotes
    if not quotes:
        ai_results = ai_service.find_chinese_quotes(keyword)
        return ai_results

    return quotes


@router.post("/", response_model=ChineseQuoteResponse)
def add_quote(quote: ChineseQuoteCreate, db: Session = Depends(get_db)):
    """Add a new Chinese quote to the database"""
    db_quote = ChineseQuote(**quote.model_dump())
    db.add(db_quote)
    db.commit()
    db.refresh(db_quote)
    return db_quote


@router.get("/browse", response_model=List[ChineseQuoteResponse])
def browse_quotes(
    era: str = Query(None),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Browse quotes by era or get random quotes"""
    query = db.query(ChineseQuote)

    if era:
        query = query.filter(ChineseQuote.era.ilike(f"%{era}%"))

    return query.limit(limit).all()
