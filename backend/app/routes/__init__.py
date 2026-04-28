from .paper_routes import router as paper_router
from .highlight_routes import router as highlight_router
from .writing_routes import router as writing_router
from .quote_routes import router as quote_router

__all__ = ["paper_router", "highlight_router", "writing_router", "quote_router"]
