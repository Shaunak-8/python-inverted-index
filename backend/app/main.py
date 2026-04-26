from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import search, documents, analytics
from app.core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title="Search Engine API",
        description="A scalable full-stack search engine with inverted index.",
        version="1.0.0"
    )

    # Setup CORS for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
    app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
    app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app

app = create_app()
