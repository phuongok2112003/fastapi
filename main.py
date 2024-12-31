from fastapi import FastAPI
from app.api.api_router import router
from app.model.model_base import Base
from app.db.session import engine
from app.core.config import settings
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI MySQL Demo")

app.include_router(router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)