from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the application."""

    # Database settings
    DATABASE_USER: str = Field(default="postgres")
    DATABASE_PASSWORD: str = Field(default="postgres")
    DATABASE_HOST: str = Field(default="localhost")
    DATABASE_PORT: int = Field(default=5432)
    DATABASE_NAME: str = Field(default="notifier_db")
    DATABASE_URL: str | None = None  # If specified, overrides the above settings

    # JWT settings
    SECRET_KEY: str = Field(default="your-secret-key")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    # Passlib CryptContext Settings
    PASSWORD_CRYPT_ALGORITHM: str = Field(default="bcrypt")
    PASSWORD_HASHING_ROUNDS: int = Field(default=12)

    class Config:
        """Config for the Settings class."""

        # load the default environment variables from the root .env file
        env_file = ".env"
        extra = "allow"

    def get_db_url(self):
        """Get the database URL.

        :return: The database URL.
        """
        return (
            self.DATABASE_URL
            or f"postgres://{self.DATABASE_USER}:{self.DATABASE_PASSWORD} "
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )


# instantiate settings to load all configurations
settings = Settings()
