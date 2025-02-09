from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.user import router as user_router
from app.api.action import router as action_router
from app.core.dependencies import get_db

from collections.abc import AsyncIterator
from fastapi.middleware.cors import CORSMiddleware

from app.db import mongo


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    print("Starting up...")

    await mongo.init_db()

    application.state.mongo = mongo


    yield
    await mongo.close_connection()

    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(action_router, prefix="/actions", tags=["actions"])

allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def _():
    return {"status": "online"}