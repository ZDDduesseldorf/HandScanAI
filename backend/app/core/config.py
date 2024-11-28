from __future__ import annotations

from pathlib import Path

from pydantic import AnyHttpUrl, AnyUrl, field_validator
from pydantic_settings import BaseSettings

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


class Environment(StrEnum):
    dev = "dev"
    prod = "prod"


class Paths:
    # backend
    ROOT_DIR: Path = Path(__file__).parent.parent.parent
    LIB_DIR: Path = ROOT_DIR / "lib"
    BASE_DIR: Path = ROOT_DIR / "app"
    STATIC_DIR: Path = BASE_DIR / "static"
    MEDIA_DIR: Path = BASE_DIR / "media"


class Settings(BaseSettings):
    @property
    def PATHS(self) -> Paths:
        return Paths()

    ENVIRONMENT: Environment = "dev"
    DEBUG: bool = False
    SERVER_HOST: AnyHttpUrl = "http://localhost:8000"  # type:ignore

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: list[str] | str) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    DATABASE_HOST: str
    DATABASE_PORT: int
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str

    @property
    def MONGO_URI(self) -> AnyUrl:
        return f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:{self.MONGO_INITDB_ROOT_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}"

    class Config:
        env_file = ".env"


settings = Settings()
