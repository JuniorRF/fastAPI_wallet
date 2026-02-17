from fastapi import FastAPI

from api.basic import router
import uvicorn
from core.config import Settings

app = FastAPI() #(docs_url=None, redoc_url=None)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
