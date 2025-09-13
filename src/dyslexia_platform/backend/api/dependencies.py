"""
FastAPI dependencies for the DyslexiaCare backend.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Generator

from ..database import get_db, SessionLocal
from config import get_settings

settings = get_settings()
security = HTTPBearer()


def get_database() -> Generator[SessionLocal, None, None]:
    """Database dependency for FastAPI routes."""
    return get_db()


def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
    """Verify admin token for protected endpoints."""
    if credentials.credentials != settings.admin_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True