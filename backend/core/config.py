from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    database_url: str

    frontend_url: str = "http://localhost:8501"
    backend_url: str = "http://127.0.0.1:8000"

    sendgrid_api_key: str

    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    token_encryption_key: str


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()