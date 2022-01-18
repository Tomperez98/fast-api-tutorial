import pydantic


class Settings(pydantic.BaseSettings):
    # TODO: When not using SQLite
    # database_password: str = "localhost"
    # database_username: str = "user"
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    HOST_DEV_DB: str
    HOST_TEST_DB: str
    EXPOSED_PORT: int
    POSTGRES_DB: str

    class Config:
        env_file = "app/config/app.env"


defined_settings = Settings()  # type: ignore
