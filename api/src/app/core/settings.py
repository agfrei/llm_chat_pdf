from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    openai_model_name: str = "gpt-3.5-turbo"

    chroma_persist_directory: str

    chunk_size: int = 1000
    chunk_overlap: int = 150
    chunk_separators: list[str] = [
        "\n\n",
        "\n",
        r"(?<=\. )",
        " ",
        "",
    ]
    chunk_markdown_separators: list[tuple[str, str]] = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]
