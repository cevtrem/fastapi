from datetime import datetime
import uuid
from app import config
from sqlalchemy import DateTime, Integer, String, func, UUID, ForeignKey
from sqlalchemy.ext.asyncio import (AsyncAttrs,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from app.custom_types import ROLE


engine = create_async_engine(config.PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):

    @property
    def id_dict(self):
        return {'id': self.id}


class Token(Base):
    __tablename__ = 'token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship('User', lazy='joined', back_populates='tokens')
    token: Mapped[uuid.UUID] = mapped_column(UUID, unique=True, server_default=func.gen_random_uuid())
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    @property
    def dict(self):
        return {'token': self.token}


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[ROLE] = mapped_column(String, default="user")
    tokens: Mapped[list[Token]] = relationship('Token', lazy='joined', back_populates='user')
    advertisements: Mapped[list["Advertisement"]] = relationship('Advertisement', lazy='joined', back_populates='user')

    @property
    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role
        }


class Advertisement(Base):
    __tablename__ = 'advertisements'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship('User', lazy='joined', back_populates='advertisements')

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'created_at': self.created_at,
            'user_id': self.user_id
        }


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()


ORM_OBJ = Advertisement | Token | User
ORM_CLS = type[Advertisement | Token | User]
