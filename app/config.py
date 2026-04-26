from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str = ""
    database_url: str = "sqlite+aiosqlite:///tmp/flaky_tests.db"
    github_token: str = ""
    slack_webhook_url: str = ""
    secret_key: str = "supersecretkey123"
    app_env: str = "development"
    azure_storage_connection_string: str = ""
    azure_keyvault_url: str = ""

    class Config:
        env_file = ".env"

settings = Settings()