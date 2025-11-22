from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Primary database connection string for deployment
    # This will load the correct Render URL
    DATABASE_URL: str

    class Config:
        env_file = ".env"


setting = Settings()

