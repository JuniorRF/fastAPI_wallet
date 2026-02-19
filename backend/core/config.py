from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Название приложения'
    description: str = 'Описание из приложения'
    version: str = '0.0'
    docs_url: str = '/docs'
    redoc_url: str = '/redoc'
    database_url: str

    class Config:
        env_file = '.env'


settings = Settings()
