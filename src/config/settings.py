from pydantic import BaseSettings


class Settings(BaseSettings):
    # TODO: When not using SQLite
    # database_password: str = "localhost"
    # database_username: str = "user"
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


defined_settings = Settings()
