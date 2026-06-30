from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parents[1]


class MongoSettings(BaseSettings):
    MONGO_PASS: str = "pass"
    MONGO_USER: str = "user"
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_DB_NAME: str = "my_db"

    @property
    def db_url(self):
        return (
            f"mongodb://{self.MONGO_USER}:{self.MONGO_PASS}@"
            f"{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB_NAME}?authSource=admin"
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    mongo_settings: MongoSettings = MongoSettings()

    GOOGLE_DISK_FOLDER_ID: str = "13d_tD5l0oczRt36_271iBHjnMdMMYRzm"
    GOOGLE_FILE_NAME: str = "titanic.csv"


settings = Settings()
