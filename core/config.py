# import os
# from dotenv import load_dotenv


from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import BaseModel


# load_dotenv()


class DatabaseConfig(BaseModel):
    # url: str = os.getenv("URL_DB")
    url: str = (
        "postgresql+asyncpg://osporter:fOtEyhe7Q*ix@nekludhelul.beget.app:5432/osport"
    )
    echo: bool = False
    echo_pool: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict()
    api_prefix: str = "/api"
    db: DatabaseConfig = DatabaseConfig()  # Инициализация поля db


settings = Settings()
