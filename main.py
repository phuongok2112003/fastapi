from fastapi import FastAPI
from app.api.api_router import router
from app.model.model_base import Base
from app.db.session import engine
from app.core.config import settings
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from app.until.exception_handler import CustomException,http_exception_handler
Base.metadata.create_all(bind=engine)


def start_application()->FastAPI:
    application=FastAPI(title="FastAPI")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],)
    application.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)
    application.include_router(router=router,prefix=settings.API_PREFIX)
    application.add_exception_handler(CustomException, http_exception_handler)
    return application

app = start_application()
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000,reload=True)