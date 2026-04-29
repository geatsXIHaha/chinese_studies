"""Essay idea generation API routes"""
from fastapi import APIRouter, HTTPException

from app.schemas import EssayIdeaGenerateRequest, EssayIdeaGenerateResponse, EssayIdeaStructured
from app.services import ai_service

router = APIRouter(prefix="/api", tags=["writing"])


@router.post("/essay-ideas", response_model=EssayIdeaGenerateResponse)
def generate_essay_ideas(request: EssayIdeaGenerateRequest):
    """Generate structured essay ideas from provided text"""
    text = (request.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    ideas = ai_service.generate_essay_ideas_structured(
        text=text,
        title=request.title,
        max_ideas=request.max_ideas,
    )

    return EssayIdeaGenerateResponse(
        ideas=[EssayIdeaStructured(**idea) for idea in ideas]
    )