from fastapi import FastAPI

from backend.core.config import settings
from backend.api.routers import main_router

app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    version=settings.version,
    docs_url="/" + settings.docs_url,
    redoc_url="/" + settings.redoc_url,
)


app.include_router(main_router)
