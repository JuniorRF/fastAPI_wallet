from fastapi import FastAPI

# from api.basic import router
from backend.core.config import settings

app = FastAPI(title=settings.app_title)  #(docs_url=None, redoc_url=None)

# app.include_router(router)

