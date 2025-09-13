"""API routes package."""

from .dyslexia import router as dyslexia_router
from .tts import router as tts_router

__all__ = ["dyslexia_router", "tts_router"]