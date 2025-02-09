from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schema import sustainability_action as sustainability_action_schema
from app.crud import crud
from app.core.dependencies import get_settings
from app.db import mongo

settings = get_settings()
router = APIRouter()
actions_crud = crud.CRUD(settings.mongo_actions_collection_name)


@router.post("/{user_id}", response_model=sustainability_action_schema.SustainabilityAction)
async def create_action(user_id: str, action: sustainability_action_schema.SustainabilityActionCreate):
    return await actions_crud.create(mongo.db, action.model_dump())

@router.get("/", response_model=list[sustainability_action_schema.SustainabilityAction])
async def list_actions():
    return await actions_crud.read_all(mongo.db)

@router.get("/{action_id}", response_model=sustainability_action_schema.SustainabilityAction)
async def get_action(action_id: str):
    action = await actions_crud.read_one(mongo.db, action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Ação não encontrada")
    return action

@router.put("/{action_id}", response_model=bool)
async def update_action(action_id: str, action: sustainability_action_schema.SustainabilityActionUpdate):

    update_data = action.model_dump(exclude_unset=True)


    return await actions_crud.update(mongo.db, action_id, update_data)

@router.delete("/{action_id}", response_model=bool)
async def delete_action(action_id: str):
    return await actions_crud.delete(mongo.db, action_id)

