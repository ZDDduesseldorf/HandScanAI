from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.lifetime import startup

from .core.config import settings
from .routes import router as api_router


def get_application() -> FastAPI:
    """Initialize the FastAPI application"""

    _app = FastAPI(
        title="backend",
        description="",
        debug=settings.DEBUG,
    )
    _app.add_middleware(
        CORSMiddleware,
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=["*"],  # this is a workaround
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(api_router)

    _app.add_event_handler("startup", startup)

    return _app


app = get_application()
