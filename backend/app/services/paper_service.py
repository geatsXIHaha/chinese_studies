"""Service for academic paper operations"""
from sqlalchemy.orm import Session
from app.models import Paper, Highlight, EssayIdea, EssayConversation, EssayMessage
from app.schemas import PaperCreate, HighlightCreate, EssayIdeaCreate
from typing import List, Optional


class PaperService:
    """Service for paper-related operations"""

    @staticmethod
    def create_paper(db: Session, paper: PaperCreate) -> Paper:
        """Create a new paper"""
        db_paper = Paper(**paper.model_dump())
        db.add(db_paper)
        db.commit()
        db.refresh(db_paper)
        return db_paper

    @staticmethod
    def get_paper(db: Session, paper_id: int) -> Optional[Paper]:
        """Get a paper by ID"""
        return db.query(Paper).filter(Paper.id == paper_id).first()

    @staticmethod
    def search_papers(db: Session, query: str, limit: int = 10) -> List[Paper]:
        """Search papers by title, authors, or keywords"""
        search_term = f"%{query}%"
        return (
            db.query(Paper)
            .filter(
                (Paper.title.ilike(search_term))
                | (Paper.authors.ilike(search_term))
                | (Paper.keywords.ilike(search_term))
            )
            .limit(limit)
            .all()
        )

    @staticmethod
    def list_papers(db: Session, skip: int = 0, limit: int = 10) -> List[Paper]:
        """List all papers with pagination"""
        return db.query(Paper).offset(skip).limit(limit).all()

    @staticmethod
    def delete_paper(db: Session, paper_id: int) -> bool:
        """Delete a paper"""
        paper = db.query(Paper).filter(Paper.id == paper_id).first()
        if paper:
            db.delete(paper)
            db.commit()
            return True
        return False


class HighlightService:
    """Service for highlight operations"""

    @staticmethod
    def create_highlight(db: Session, highlight: HighlightCreate) -> Highlight:
        """Create a new highlight"""
        db_highlight = Highlight(**highlight.model_dump())
        db.add(db_highlight)
        db.commit()
        db.refresh(db_highlight)
        return db_highlight

    @staticmethod
    def get_highlights_for_paper(
        db: Session, paper_id: int, user_id: str
    ) -> List[Highlight]:
        """Get all highlights for a paper by user"""
        return (
            db.query(Highlight)
            .filter(Highlight.paper_id == paper_id, Highlight.user_id == user_id)
            .all()
        )

    @staticmethod
    def update_highlight_explanation(
        db: Session, highlight_id: int, explanation: str
    ) -> Optional[Highlight]:
        """Update highlight with AI explanation"""
        highlight = db.query(Highlight).filter(Highlight.id == highlight_id).first()
        if highlight:
            highlight.explanation = explanation
            db.commit()
            db.refresh(highlight)
        return highlight

    @staticmethod
    def delete_highlight(db: Session, highlight_id: int) -> bool:
        """Delete a highlight"""
        highlight = db.query(Highlight).filter(Highlight.id == highlight_id).first()
        if highlight:
            db.delete(highlight)
            db.commit()
            return True
        return False


class EssayIdeaService:
    """Service for essay idea operations"""

    @staticmethod
    def create_essay_idea(db: Session, idea: EssayIdeaCreate) -> EssayIdea:
        """Create a new essay idea"""
        db_idea = EssayIdea(**idea.model_dump())
        db.add(db_idea)
        db.commit()
        db.refresh(db_idea)
        return db_idea

    @staticmethod
    def get_essay_ideas_for_paper(
        db: Session, paper_id: int, user_id: str
    ) -> List[EssayIdea]:
        """Get all essay ideas for a paper by user"""
        return (
            db.query(EssayIdea)
            .filter(EssayIdea.paper_id == paper_id, EssayIdea.user_id == user_id)
            .all()
        )

    @staticmethod
    def delete_essay_idea(db: Session, idea_id: int) -> bool:
        """Delete an essay idea"""
        idea = db.query(EssayIdea).filter(EssayIdea.id == idea_id).first()
        if idea:
            db.delete(idea)
            db.commit()
            return True
        return False


class EssayConversationService:
    """Service for essay idea chat conversations"""

    @staticmethod
    def create_conversation(
        db: Session, paper_id: int, user_id: str, idea_topic: str | None
    ) -> EssayConversation:
        conversation = EssayConversation(
            paper_id=paper_id, user_id=user_id, idea_topic=idea_topic
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation(db: Session, conversation_id: int) -> EssayConversation | None:
        return (
            db.query(EssayConversation)
            .filter(EssayConversation.id == conversation_id)
            .first()
        )


class EssayMessageService:
    """Service for essay idea chat messages"""

    @staticmethod
    def add_message(
        db: Session, conversation_id: int, role: str, content: str
    ) -> EssayMessage:
        message = EssayMessage(
            conversation_id=conversation_id, role=role, content=content
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def list_messages(db: Session, conversation_id: int) -> List[EssayMessage]:
        return (
            db.query(EssayMessage)
            .filter(EssayMessage.conversation_id == conversation_id)
            .order_by(EssayMessage.created_at.asc())
            .all()
        )
