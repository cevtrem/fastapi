from fastapi import FastAPI, HTTPException
from datetime import datetime
from app import crud
from app import auth
from app import models
from app.schema import (CreateAdvertisementResponse, CreateAdvertisementRequest, GetAdvertisementResponse,
                    DeleteAdvertisementResponse, UpdateAdvertisementResponse, UpdateAdvertisementRequest,
                    SearchAdvertisementResponse, LoginRequest, LoginResponse, CreateUserRequest,
                    CreateUserResponse, GetUserResponse, UpdateUserRequest, DeleteUserResponse)
from app.lifespan import lifespan
from app.dependancy import SessionDependency, TokenDependency, OptionalTokenDependency
from sqlalchemy import select, func
from app.constants import SUCCESS_RESPONCE


app = FastAPI(
    title='advertisement',
    description='Online bulletin board',
    lifespan=lifespan
)


@app.post('/advertisement', response_model=CreateAdvertisementResponse)
async def create_advertisement(advertisement: CreateAdvertisementRequest, session: SessionDependency, token: TokenDependency):
    ad_data = advertisement.model_dump()
    if ad_data.get('created_at') is None:
        ad_data['created_at'] = datetime.now()
    to_orm_obj = models.Advertisement(**ad_data, user_id=token.user_id)
    await crud.add_item(session, to_orm_obj)
    return to_orm_obj.id_dict


@app.get('/advertisement', tags=['advertisement'], response_model=SearchAdvertisementResponse)
async def searsh_advertisement_by_query(session: SessionDependency, query: str):
    query = (
        select(models.Advertisement)
        .where(models.Advertisement.title.ilike(f"%{query}%"))
        .limit(10000)
    )
    advers = await session.scalars(query)
    return {'results': [adver.dict for adver in advers]}


@app.get('/advertisement/{advertisement_id}', tags=['advertisement'], response_model=GetAdvertisementResponse)
async def get_advertisement_by_id(advertisement_id: int, session: SessionDependency):
    to_orm_obj = await crud.get_item_by_id(session, models.Advertisement, advertisement_id)
    return to_orm_obj.dict


@app.patch('/advertisement/{advertisement_id}', tags=['advertisement'], response_model=UpdateAdvertisementResponse)
async def update_advertisement(advertisement_id: int, advertisement_data: UpdateAdvertisementRequest, session: SessionDependency, token: TokenDependency):
    to_dict = advertisement_data.model_dump(exclude_unset=True)
    to_orm_obj = await crud.get_item_by_id(session, models.Advertisement, advertisement_id)
    if token.user.role == "admin" or to_orm_obj.user_id == token.user_id:
        for field, value in to_dict.items():
            setattr(to_orm_obj, field, value)
        await crud.add_item(session, to_orm_obj)
        return SUCCESS_RESPONCE
    raise HTTPException(status_code=403, detail="Not enough permissions")


@app.delete('/advertisement/{advertisement_id}', tags=['advertisement'], response_model=DeleteAdvertisementResponse)
async def delete_advertisement(advertisement_id: int, session: SessionDependency, token: TokenDependency):
    to_orm_obj = await crud.get_item_by_id(session, models.Advertisement, advertisement_id)
    if not to_orm_obj:
        raise HTTPException(status_code=404, detail="Item not found")
    if token.user.role == "admin" or to_orm_obj.user_id == token.user_id:
        await crud.delete_item(session, to_orm_obj)
        return SUCCESS_RESPONCE
    raise HTTPException(status_code=403, detail="Not enough permissions")


@app.post('/login', tags=['login'], response_model=LoginResponse)
async def login(login_data: LoginRequest, session: SessionDependency):
    query = (
        select(models.User)
        .where(models.User.name == login_data.name)
    )
    user = await session.scalar(query)
    if not user or not auth.check_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = models.Token(user_id=user.id)
    await crud.add_item(session, token)
    return token.dict

@app.get('/user/{user_id}', tags=['user'], response_model=GetUserResponse)
async def get_user(user_id: int, session: SessionDependency):
    user = await crud.get_item_by_id(session, models.User, user_id)
    if user:
        return user.dict
    raise HTTPException(status_code=404, detail="User not found")

@app.post('/user', tags=['user'], response_model=CreateUserResponse)
async def create_user(user_data: CreateUserRequest, session: SessionDependency, token: OptionalTokenDependency = None):
    user_dict = user_data.model_dump()
    user_dict['password'] = auth.hash_password(user_dict['password'])
    # Accept provided role or default to 'user'
    if user_dict.get('role') is None:
        user_dict['role'] = 'user'
    user_orm_obj = models.User(**user_dict)
    await crud.add_item(session, user_orm_obj)
    return user_orm_obj.id_dict

@app.patch('/user/{user_id}', tags=['user'], response_model=GetUserResponse)
async def update_user(user_id: int, user_data: UpdateUserRequest, session: SessionDependency, token: TokenDependency):
    user = await crud.get_item_by_id(session, models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if token.user.role == "admin" or user.id == token.user_id:
        user_dict = user_data.model_dump(exclude_unset=True)
        if 'password' in user_dict and user_dict['password'] is not None:
            user_dict['password'] = auth.hash_password(user_dict['password'])
        if 'role' in user_dict and user_dict['role'] is not None and token.user.role != 'admin':
            raise HTTPException(status_code=403, detail="Not enough permissions to change role")
        for field, value in user_dict.items():
            setattr(user, field, value)
        await crud.add_item(session, user)
        return user.dict
    raise HTTPException(status_code=403, detail="Not enough permissions")

@app.delete('/user/{user_id}', tags=['user'], response_model=DeleteUserResponse)
async def delete_user(user_id: int, session: SessionDependency, token: TokenDependency):
    user = await crud.get_item_by_id(session, models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if token.user.role == "admin" or user.id == token.user_id:
        await crud.delete_item(session, user)
        return {"status": "success"}
    raise HTTPException(status_code=403, detail="Not enough permissions")
