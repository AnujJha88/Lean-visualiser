"""
Lean Proof Visualizer - Backend

FastAPI application for analyzing Lean 4 proofs.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import proof_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title="Lean Proof Visualizer API",
        description="Analyze Lean 4 proofs and visualize state evolution",
        version="0.1.0",
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(proof_router)
    
    # Health check
    @app.get("/health")
    async def health():
        return {"status": "healthy", "service": "lean-visualizer"}
    
    @app.get("/")
    async def root():
        return {
            "message": "Lean Proof Visualizer API",
            "docs": "/docs",
            "health": "/health"
        }
    
    return app


app = create_app()
