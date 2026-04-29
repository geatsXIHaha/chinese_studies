from .paper_routes import router as paper_router
from .highlight_routes import router as highlight_router
from .writing_routes import router as writing_router
from .quote_routes import router as quote_router
from .essay_routes import router as essay_router
from .essay_chat_routes import router as essay_chat_router
from .find_source_routes import router as find_source_router

__all__ = [
	"paper_router",
	"highlight_router",
	"writing_router",
	"quote_router",
	"essay_router",
	"essay_chat_router",
	"find_source_router",
]
