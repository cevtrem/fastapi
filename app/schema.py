import datetime
from pydantic import BaseModel
from typing import Literal
import uuid


class SuccessResponse(BaseModel):
    status: Literal['success']


class CreateAdvertisementResponse(BaseModel):
    id: int


class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int
    created_at: datetime.datetime


class SearchAdvertisementResponse(BaseModel):
    results: list[GetAdvertisementResponse]


class UpdateAdvertisementResponse(SuccessResponse):
    pass


class DeleteAdvertisementResponse(SuccessResponse):
    pass


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: int    


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None


class LoginRequest(BaseModel):
    name: str
    password: str


class LoginResponse(BaseModel):
    token: uuid.UUID


class CreateUserRequest(BaseModel):
    name: str
    password: str
    role: Literal['user', 'admin'] | None = None


class CreateUserResponse(BaseModel):
    id: int


class GetUserResponse(BaseModel):
    id: int
    name: str
    role: str

class UpdateUserRequest(BaseModel):
    name: str | None = None
    password: str | None = None
    role: Literal['user', 'admin'] | None = None

class DeleteUserResponse(SuccessResponse):
    pass