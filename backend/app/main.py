"""Main FastAPI application"""
import os

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import init_db

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from app.routes import paper_router, highlight_router, writing_router, quote_router

# Initialize database
init_db()

app = FastAPI(
    title="Chinese Academic AI Study System",
    description="A full-stack application for academic paper analysis with AI assistance",
    version="1.0.0",
)

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


def _get_cors_origins() -> list[str]:
    origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").strip()
    if not origins:
        return ["http://localhost:3000"]
    return [origin.strip() for origin in origins.split(",") if origin.strip()]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(paper_router)
app.include_router(highlight_router)
app.include_router(writing_router)
app.include_router(quote_router)


@app.get("/")
def root():
    """Welcome endpoint"""
    return {
        "name": "Chinese Academic AI Study System",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
