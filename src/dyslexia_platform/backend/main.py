"""
Main FastAPI application for DyslexiaCare backend.
"""

import sys
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import get_settings
from src.dyslexia_platform.database import create_tables
from src.dyslexia_platform.backend.api.routes import dyslexia_router, tts_router
from src.dyslexia_platform.backend.models.schemas import HealthResponse, ErrorResponse
from src.dyslexia_platform.shared.utils import setup_logging

settings = get_settings()

# Setup logging
logger = setup_logging(
    log_level="INFO" if not settings.debug else "DEBUG",
    log_file=settings.get_logs_path() / "backend.log"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting DyslexiaCare backend...")
    
    # Create database tables
    try:
        create_tables()
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    
    # Ensure required directories exist
    settings.get_upload_path().mkdir(parents=True, exist_ok=True)
    settings.get_output_path().mkdir(parents=True, exist_ok=True)
    settings.get_logs_path().mkdir(parents=True, exist_ok=True)
    
    logger.info("DyslexiaCare backend started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down DyslexiaCare backend...")


# Create FastAPI application
app = FastAPI(
    title="DyslexiaCare API",
    description="AI-powered dyslexia screening and accessibility platform",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dyslexia_router, prefix="/api/v1")
app.include_router(tts_router, prefix="/api/v1")


# Health check endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with basic service information."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version=settings.app_version
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version=settings.app_version
    )


@app.get("/api/v1/info")
async def api_info():
    """API information and capabilities."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "AI-powered dyslexia screening and accessibility platform",
        "endpoints": {
            "dyslexia_analysis": "/api/v1/dyslexia/analyze",
            "text_to_speech": "/api/v1/tts/synthesize",
            "capabilities": "/api/v1/tts/capabilities"
        },
        "features": [
            "Multi-modal dyslexia screening",
            "Text-to-speech with accessibility features",
            "Handwriting analysis via OCR",
            "Speech fluency assessment",
            "Phonics mode support",
            "Multiple language support"
        ],
        "documentation": "/docs" if settings.debug else "Contact administrator"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal Server Error",
            message="An unexpected error occurred",
            details={"type": type(exc).__name__} if settings.debug else None,
            timestamp=datetime.now().isoformat()
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level="info" if not settings.debug else "debug"
    )