from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'OOO "ИТК" кошелёк'

    class Config:
        env_file = '.env'


settings = Settings()
