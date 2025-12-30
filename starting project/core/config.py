from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    debug: bool = False

    # آدرس فایل .env را اینجا مشخص می‌کنید
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()