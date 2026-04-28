"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PaperBase(BaseModel):
    title: str
    authors: str
    abstract: str
    full_text: str
    publication_date: Optional[datetime] = None
    source_url: Optional[str] = None
    doi: Optional[str] = None
    keywords: Optional[str] = None


class PaperCreate(PaperBase):
    pass


class PaperResponse(PaperBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HighlightBase(BaseModel):
    paper_id: int
    user_id: str
    text: str
    start_position: int
    end_position: int


class HighlightCreate(HighlightBase):
    pass


class HighlightResponse(HighlightBase):
    id: int
    explanation: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class EssayIdeaBase(BaseModel):
    paper_id: int
    user_id: str
    idea: str
    keywords: Optional[str] = None


class EssayIdeaCreate(EssayIdeaBase):
    pass


class EssayIdeaResponse(EssayIdeaBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChineseQuoteBase(BaseModel):
    quote: str
    source: str
    author: Optional[str] = None
    era: Optional[str] = None
    meaning: Optional[str] = None


class ChineseQuoteCreate(ChineseQuoteBase):
    pass


class ChineseQuoteResponse(ChineseQuoteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TextExplanationRequest(BaseModel):
    text: str
    context: Optional[str] = None


class TextExplanationResponse(BaseModel):
    original_text: str
    explanation: str
    key_terms: List[str]


class TranslateRequest(BaseModel):
    text: str
    target_language: str = "en"


class TranslateResponse(BaseModel):
    original_text: str
    translated_text: str


class WriteHumaniserRequest(BaseModel):
    text: str


class WriteHumaniserResponse(BaseModel):
    original_text: str
    humanised_text: str
