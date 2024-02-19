from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_INITDB_DATABASE: str
    DATABASE_URL: str
    
    VERSION_API: str
    
    LOGIN: str
    PASSWORD: str

    SMTP_SERVER: str
    SMTP_PORT: str
    SMTP_USERNAME: str
    SMTP_PASSWORD: str

    class Config:
        env_file = '.env'


settings = Settings()