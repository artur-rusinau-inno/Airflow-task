from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parents[1]


class MongoSettings(BaseSettings):
    MONGO_PASS: str = "pass"
    MONGO_USER: str = "user"
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_DB_NAME: str = "my_db"
    MONGO_COLLECTION_NAME: str = "user_reviews"
    MONGO_PARAMS: dict = {
        "mongo_collection": MONGO_COLLECTION_NAME,
        "mongo_db": MONGO_DB_NAME,
    }

    @property
    def db_url(self):
        return (
            f"mongodb://{self.MONGO_USER}:{self.MONGO_PASS}@"
            f"{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB_NAME}?authSource=admin"
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    mongo_settings: MongoSettings = MongoSettings()

    GDRIVE_FOLDER_ID: str = "13d_tD5l0oczRt36_271iBHjnMdMMYRzm"
    GDRIVE_FILE_NAME: str = "raw_data.csv"
    GDRIVE_PARAMS: dict = {"folder_id": GDRIVE_FOLDER_ID, "file_name": GDRIVE_FILE_NAME}
    LOCAL_FILE_PATH: str = str(BASE_DIR / "data" / "transformed_data.csv")


settings = Settings()
