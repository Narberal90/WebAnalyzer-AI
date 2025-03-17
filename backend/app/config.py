from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    OPENAI_API_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str

    POSTGRES_HOST: str = "db"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    ASYNC_DATABASE_URL: str = ""
    SYNC_DATABASE_URL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ASYNC_DATABASE_URL = (
            "postgresql+asyncpg://{user}:{password}@{host}/{db}".format(
                user=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                db=self.POSTGRES_DB,
            )
        )
        self.SYNC_DATABASE_URL = (
            "postgresql://{user}:{password}@{host}/{db}".format(
                user=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                db=self.POSTGRES_DB,
            )
        )


settings = Settings()
