from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Any, Dict, List
from datetime import datetime
from app.schema.identificator import PyObjectId


def to_object_id(_id: str) -> PyObjectId:
    try:
        _id = PyObjectId(
            ObjectId(_id)
        )
        return _id
    except:
        raise ValueError("Invalid ObjectId")


class CRUD:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name


    async def create(self, db: AsyncIOMotorDatabase, data: Dict[str, Any]) -> Dict[str, Any]:
        result = await db[self.collection_name].insert_one(data)

        _id = result.inserted_id
        created_at = datetime.now()
        updated_at = datetime.now()

        await self.update(db, _id, {"created_at": created_at})

        data["_id"] = _id
        data["created_at"] = created_at
        data["updated_at"] = updated_at
        return data

    async def read_all(self, db: AsyncIOMotorDatabase, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        cursor = db[self.collection_name].find({}).skip(skip).limit(limit)
        documents = []
        async for doc in cursor:
            doc["_id"] = str(doc.pop("_id"))
            documents.append(doc)

        return documents

    async def read_one(self, db: AsyncIOMotorDatabase, id: str) -> Dict[str, Any] or None:
        document = await db[self.collection_name].find_one({"_id": to_object_id(id)})
        if not document:
            return None
        document["_id"] = str(document.pop("_id"))
        return document

    async def update(self, db: AsyncIOMotorDatabase, id: str, data: Dict[str, Any]) -> bool:
        # data["updated_at"] = datetime.now()
        result = await db[self.collection_name].update_one(
            {"_id": to_object_id(id)},
            {
                "$set": data,
            },
        )
        print(result.raw_result)
        return result.matched_count > 0

    async def delete(self, db: AsyncIOMotorDatabase, id: str) -> bool:
        result = await db[self.collection_name].delete_one({"_id": to_object_id(id)})
        return result.deleted_count > 0
