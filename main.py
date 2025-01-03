from fastapi import FastAPI
from app.api.api_router import router
from app.model.model_base import Base
from app.db.session import engine
from app.core.config import settings
import uvicorn
from starlette.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)





def start_application()->FastAPI:
    application=FastAPI(title="FastAPI")
    application.include_router(router=router,prefix=settings.API_PREFIX)
    return application

app = start_application()
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000,reload=True)