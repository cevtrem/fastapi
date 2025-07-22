from fastapi import FastAPI
from datetime import datetime
import crud
import models
from schema import (CreateAdvertisementResponce, CreateAdvertisementRequest, GetAdvertisementResponce,
                    DeleteAdvertisementResponce, UpdateAdvertisementResponce, UpdateAdvertisementRequest,
                    SearshAdvertisementResponce
                    )
from lifespan import lifespan
from dependancy import SessionDependency
from sqlalchemy import select
from constants import SUCCESS_RESPONCE


app = FastAPI(
    title='advertisement',
    description='Online bulletin board',
    lifespan=lifespan
)


@app.post('/advertisement', response_model=CreateAdvertisementResponce)
async def create_advertisement(advertisement: CreateAdvertisementRequest, session: SessionDependency):
    ad_data = advertisement.model_dump()
    if ad_data.get('created_at') is None:
        ad_data['created_at'] = datetime.now()
    to_orm_obj = models.Advertisement(**ad_data)
    await crud.add_item(session, to_orm_obj)
    return to_orm_obj.id_dict


@app.get('/advertisement/{advertisement_id}', tags=['advertisement'], response_model=GetAdvertisementResponce)
async def get_advertisement(advertisement_id: int, session: SessionDependency):
    to_orm_obj = await crud.get_item_by_id(session, models.Advertisement, advertisement_id)
    return to_orm_obj.dict


@app.get('/advertisement/', tags=['advertisement'], response_model=SearshAdvertisementResponce)
async def searsh_advertisement(session: SessionDependency, title: str):
    query = (
        select(models.Advertisement)
        .where(models.Advertisement.title == title)
        .limit(10000)
    )
    advers = await session.scalars(query)
    return {'results': [adver.dict for adver in advers]}


@app.patch('/advertisement/{advertisement_id}', tags=['advertisement'], response_model=UpdateAdvertisementResponce)
async def update_advertisement(advertisement_id: int, advertisement_data: UpdateAdvertisementRequest, session: SessionDependency):
    to_dict = advertisement_data.model_dump(exclude_unset=True)
    to_orm_obj = await crud.get_item_by_id(session, models.Advertisement, advertisement_id)

    for field, value in to_dict.items():
        setattr(to_orm_obj, field, value)
    await crud.add_item(session, to_orm_obj)
    return SUCCESS_RESPONCE


@app.delete('/advertisement/{advertisement_id}', tags=['advertisement'], response_model=DeleteAdvertisementResponce)
async def delete_advertisement(advertisement_id: int, session: SessionDependency):
    to_orm_obj = await crud.get_item_by_id(session, models.Advertisement, advertisement_id)
    await crud.delete_item(session, to_orm_obj)
    return SUCCESS_RESPONCE
