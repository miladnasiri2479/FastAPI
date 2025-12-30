from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # postgres envs
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./sqlite.db"
    
settings = Settings()