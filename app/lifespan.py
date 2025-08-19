from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.models import close_orm, init_orm


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('START')
    await init_orm()
    yield
    await close_orm()
    print('FINISH')
