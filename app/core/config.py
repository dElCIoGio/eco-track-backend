from pydantic import Field, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseSettings):
    mongo_uri: str = Field(alias="MONGO_URI", default="mongodb+srv://dagostinho4:gfrpWLjBlls4T9uW@database.ehsjf.mongodb.net/?retryWrites=true&w=majority&appName=database")
    mongo_db_name: str = Field(alias="MONGO_DB_NAME", default="database")
    mongo_users_collection_name: str = Field(
        alias="MONGO_USERS_COLLECTION_NAME", default="users"
    )
    mongo_actions_collection_name: str = Field(
        alias="MONGO_ACTIONS_COLLECTION_NAME", default="sustainability actions"
    )

class Settings(MongoSettings):  # Inherits both Mongo and Firebase settings
    pass


settings = Settings()
