import datetime
from pydantic import BaseModel
from typing import Literal


class SuccessResponse(BaseModel):
    status: Literal['success']


class CreateAdvertisementResponce(BaseModel):
    id: int


class GetAdvertisementResponce(BaseModel):
    id: int
    title: str
    description: str
    price: int
    owner: str
    created_at: datetime.datetime


class SearshAdvertisementResponce(BaseModel):
    results: list[GetAdvertisementResponce]


class UpdateAdvertisementResponce(SuccessResponse):
    pass


class DeleteAdvertisementResponce(SuccessResponse):
    pass


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: int
    owner: str


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    owner: str | None = None
