
import os
import sys

from pymongo.errors import PyMongoError
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname('app'), '..')))

from motor.motor_asyncio import AsyncIOMotorClient as MongoClient, AsyncIOMotorDatabase
from app.core.config import settings
from beanie import init_beanie
from app.schema import user, sustainability_action

class MongoDB:
    """A MongoDB utility class for managing the database connection."""

    def __init__(self):
        self.client: MongoClient | None = None
        self.db: AsyncIOMotorDatabase | None = None



    async def init_db(self) -> None:
        """
        Initialize the MongoDB client and database connection,
        and set up Beanie with the specified document models.
        """
        try:
            self.client = MongoClient(settings.mongo_uri)
            self.db = self.client[settings.mongo_db_name]

            self.ping()

            document_models = [user.UserDocument, sustainability_action.SustainabilityActionDocument]
            await init_beanie(database=self.db, document_models=document_models)
            print("MongoDB connection established and Beanie initialized.")
        except Exception as e:
            print(f"Error initializing MongoDB: {e}")
            raise

    async def close_connection(self) -> None:
        """
        Close the MongoDB client connection.
        """
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

    def ping(self) -> None:
        """
        Ping the MongoDB server to verify the connection.
        """
        try:

            self.client.admin.command('ping')
            print("Pinged MongoDB deployment successfully.")
        except PyMongoError as e:
            print(f"Failed to ping MongoDB: {e}")
            raise

    def get_db(self) -> AsyncIOMotorDatabase:
        """
        Get the MongoDB database instance.
        """
        if self.db == None:
            raise ValueError("Database not initialized. Call init_db() first.")
        return self.db

    def get_client(self) -> MongoClient:
        """
        Get the MongoDB client instance.
        """
        if not self.client:
            raise ValueError("Client not initialized. Call init_db() first.")
        return self.client


# Instantiate a shared MongoDB instance
mongo = MongoDB()

__all__ = [
    "mongo",
    "MongoDB",
]