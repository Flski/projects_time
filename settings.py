from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
  JWT_SECRET_KEY: str
  JWT_ACCESS_COOKIE_NAME: str
  model_config = SettingsConfigDict(
    env_file=os.path.join(os.path.dirname(__file__), ".env"),
    env_file_encoding="UTF-8"
  )

settings = Settings()
