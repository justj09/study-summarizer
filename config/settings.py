import json
from typing import Mapping
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="config/.env")

    google_account_file: str
    openai_key: str
    gpt_model: str
    
    api_key: str
    temp_folder: str = "./temp"
    max_file_size_mb: int = 10
    max_page_count: int = 50

    @computed_field
    @property
    def google_credentials(self) -> Mapping[str, str]:
        with open(self.google_account_file, "r", encoding="utf-8") as f:
            return json.load(f)
