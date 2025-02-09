from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schema import user as user_schema
from app.crud import crud
from app.core.dependencies import get_settings
from app.db import mongo
from app.schema.user import UserCreate
from app.schema import sustainability_action as sustainability_action_crud


settings = get_settings()
router = APIRouter()
user_crud = crud.CRUD(settings.mongo_users_collection_name)


@router.post("/", response_model=user_schema.User)
async def create_user(user: UserCreate):

    return await user_crud.create(mongo.db, user.model_dump())

@router.get("/", response_model=list[user_schema.User])
async def list_users():
    return await user_crud.read_all(mongo.db)

@router.get("/{user_id}", response_model=user_schema.User)
async def get_user(user_id: str):
    user = await user_crud.read_one(mongo.db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.put("/{user_id}", response_model=bool)
async def update_user(user_id: str, user: UserCreate):
    return await user_crud.update(mongo.db, user_id, user.dict())

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    return await user_crud.delete(mongo.db, user_id)

@router.get("/{user_id}/actions", response_model=list[sustainability_action_crud.SustainabilityAction])
async def get_user_actions(user_id: str):
    return await sustainability_action_crud.SustainabilityActionDocument.find({"user_id": user_id}).to_list()


@router.get("/{firebase_auth_id}/firebase", response_model=user_schema.User)
async def get_action_token(firebase_auth_id: str):
    return await user_schema.UserDocument.find_one({"firebase_uid": firebase_auth_id})