from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Фонд QRKot'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
