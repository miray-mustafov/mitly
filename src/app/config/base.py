from pydantic_settings import BaseSettings, SettingsConfigDict


class AppBaseSettings(BaseSettings):
    """
    Pydantic automatically reads environment variables from a .env file if it exists, else it uses the defaults.
    """
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DEFAULT_URL_EXPIRY_DAYS: int = 30

    ENV: str = "dev"
    DB_DIALECT: str = "postgresql"
    DB_DRIVER: str = "psycopg"
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_HOST: str = "localhost"
    DB_NAME: str = "mittly_db"
