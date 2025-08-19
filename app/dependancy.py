from typing import Annotated
import uuid
from fastapi import Depends, Header, HTTPException
from app.models import Session, Token
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import TOKEN_TTL_SEC
import datetime

async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_session, use_cache=True)]


async def get_token(x_token: Annotated[uuid.UUID, Header()], session: SessionDependency) -> Token:
    query = (
        select(Token)
        .where(Token.token == x_token,
               Token.created_at >= (datetime.datetime.now() - datetime.timedelta(seconds=TOKEN_TTL_SEC))
               )
    )
    token = await session.scalar(query)
    if token is None:
        raise HTTPException(status_code=401, detail="Token not found or expired")
    return token

TokenDependency = Annotated[Token, Depends(get_token)]


async def get_optional_token(x_token: Annotated[uuid.UUID | None, Header()] = None, session: SessionDependency = None) -> Token | None:
    if x_token is None:
        return None
    query = (
        select(Token)
        .where(Token.token == x_token,
               Token.created_at >= (datetime.datetime.now() - datetime.timedelta(seconds=TOKEN_TTL_SEC))
               )
    )
    token = await session.scalar(query)
    if token is None:
        raise HTTPException(status_code=401, detail="Token not found or expired")
    return token

OptionalTokenDependency = Annotated[Token | None, Depends(get_optional_token)]
