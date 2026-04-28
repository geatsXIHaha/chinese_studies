"""Paper model for database"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base


class Paper(Base):
    """Academic paper model"""
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), index=True)
    authors = Column(String(500))
    abstract = Column(Text)
    full_text = Column(Text)
    source_url = Column(String(500))
    publication_date = Column(DateTime, default=datetime.utcnow)
    doi = Column(String(100), unique=True, nullable=True)
    keywords = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Highlight(Base):
    """User highlights on papers"""
    __tablename__ = "highlights"

    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, index=True)
    user_id = Column(String(50), index=True)
    text = Column(Text)
    explanation = Column(Text, nullable=True)
    start_position = Column(Integer)
    end_position = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EssayIdea(Base):
    """Generated essay ideas"""
    __tablename__ = "essay_ideas"

    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, index=True)
    user_id = Column(String(50), index=True)
    idea = Column(Text)
    keywords = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ChineseQuote(Base):
    """Chinese quotes and sources"""
    __tablename__ = "chinese_quotes"

    id = Column(Integer, primary_key=True, index=True)
    quote = Column(Text)
    source = Column(String(300))
    author = Column(String(100))
    era = Column(String(100))
    meaning = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
