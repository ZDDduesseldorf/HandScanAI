from __future__ import annotations

from pathlib import Path
from typing import Union

from pydantic import AnyHttpUrl, field_validator
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


class Settings(BaseSettings):
    @property
    def PATHS(self) -> Paths:
        return Paths()

    ENVIRONMENT: Environment = "dev"
    DEBUG: bool = False
    SERVER_HOST: AnyHttpUrl = "http://localhost:8000"  # type:ignore

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, list[str]]) -> Union[list[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = ".env"


settings = Settings()
