"""Essay idea chat API routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import EssayChatRequest, EssayChatResponse, EssayChatMessage
from app.services import (
    ai_service,
    PaperService,
    EssayConversationService,
    EssayMessageService,
)

router = APIRouter(prefix="/api/essay-ideas", tags=["writing"])


@router.post("/chat", response_model=EssayChatResponse)
def chat_essay_idea(request: EssayChatRequest, db: Session = Depends(get_db)):
    text = (request.message or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Message is required")

    paper = PaperService.get_paper(db, request.paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    conversation = None
    if request.conversation_id:
        conversation = EssayConversationService.get_conversation(
            db, request.conversation_id
        )
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

    if not conversation:
        conversation = EssayConversationService.create_conversation(
            db,
            paper_id=request.paper_id,
            user_id=request.user_id,
            idea_topic=request.idea_topic,
        )

    EssayMessageService.add_message(
        db, conversation_id=conversation.id, role="user", content=text
    )

    reply = ai_service.elaborate_essay_idea(
        idea_topic=conversation.idea_topic or request.idea_topic or "",
        user_message=text,
        paper_title=paper.title,
        paper_context=paper.abstract or paper.full_text,
    )

    EssayMessageService.add_message(
        db, conversation_id=conversation.id, role="assistant", content=reply
    )

    messages = EssayMessageService.list_messages(db, conversation.id)
    return EssayChatResponse(
        conversation_id=conversation.id,
        reply=reply,
        messages=[
            EssayChatMessage(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at,
            )
            for msg in messages
        ],
    )