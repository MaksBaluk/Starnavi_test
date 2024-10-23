from dotenv import find_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS:int

    @property
    def get_postgres_url(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def get_sqlite_url(self):
        return f"sqlite:///{self.DB_NAME}.db"

    class Config:
        env_file = find_dotenv(".env")


settings = Settings()
