import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from fastapi.security import HTTPBearer

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

auth=  HTTPBearer(
    scheme_name='Authorization'
)
class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'FASTAPI BASE')
    SECRET_KEY: str = os.getenv('SECRET_KEY', '')
    API_PREFIX: str = ''
    BACKEND_CORS_ORIGINS: list[str] = ['*']
    DATABASE_URL: str = os.getenv('SQL_DATABASE_URL', '')
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # Token hết hạn sau 7 ngày
    SECURITY_ALGORITHM: str = 'HS256'
    LOGGING_CONFIG_FILE: str = os.path.join(BASE_DIR, 'logging.ini')
   

settings = Settings()
