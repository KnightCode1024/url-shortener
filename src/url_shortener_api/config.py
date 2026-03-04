from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent
ENV_PATH = BASE_DIR / ".env"


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
    )

    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str

    @property
    def get_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database: DatabaseConfig = DatabaseConfig()


def create_config() -> Config:
    return Config()


config = create_config()
