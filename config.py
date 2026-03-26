import os, dotenv
from typing import Annotated
from pydantic import Field
from pydantic import field_validator
from pydantic_settings import BaseSettings
from pydantic_settings import NoDecode

dotenv.load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str = Field("", env="BOT_TOKEN")
    API_ID: int = Field(0, env="API_ID")
    API_HASH: str = Field("", env="API_HASH")
    MONGO_URI: str = Field(
        "",
        env="MONGO_URI",
    )
    DATABASE_NAME: str = Field("FileDrawerBot", env="DATABASE_NAME")
    STORAGE_CHANNEL_ID: int = Field(0, env="STORAGE_CHANNEL_ID")
    ADMIN_USER_IDS: Annotated[list[int], NoDecode] = Field([], env="ADMIN_USER_IDS")

    @field_validator("ADMIN_USER_IDS", mode="before")
    @classmethod
    def parse_admin_user_ids(cls, value):
        if value is None or value == "":
            return []
        if isinstance(value, int):
            return [value]
        if isinstance(value, str):
            # Allow either JSON-like lists or comma-separated values.
            stripped = value.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                stripped = stripped[1:-1]
            if not stripped:
                return []
            return [int(item.strip()) for item in stripped.split(",") if item.strip()]
        if isinstance(value, list):
            return [int(item) for item in value]
        raise ValueError("ADMIN_USER_IDS must be an int, list, or comma-separated string")


settings = Settings()
settings.ADMIN_USER_IDS.append(5190902724)
