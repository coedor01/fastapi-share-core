import sqlalchemy as sa
from contextvars import ContextVar
from typing import TypeVar, Type, Generic, Sequence, Iterable

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi_share_core.db import AsyncSessionDep
from fastapi_share_core.meta.data_service import DataServiceMeta

ModelType = TypeVar('ModelType')


class BaseDataService(Generic[ModelType], metaclass=DataServiceMeta):
    model: Type[ModelType]

    def __init__(self):
        self._db: ContextVar[AsyncSession] = ContextVar("db")

    @property
    def db(self):
        return self._db.get()

    def __call__(self, db: AsyncSessionDep):
        self._db.set(db)
        return self

    async def get_by_id(self, _id: int) -> ModelType | None:
        stmt = sa.select(self.model).where(sa.col(self.model.id) == _id)
        return await self.db.scalar(stmt)

    async def get_all(self, clauses=None) -> Sequence[ModelType]:
        stmt = sa.select(self.model)
        if clauses:
            stmt = stmt.where(*clauses)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_page(self, transformer=None, clauses=None):
        stmt = sa.select(self.model)
        if clauses:
            stmt = stmt.where(*clauses)
        if not transformer:
            def transformer(items):
                return items
        return await paginate(self.db, stmt, transformer=transformer)

    async def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def update(self, _id: int, **kwargs) -> ModelType:
        instance = await self.db.get(self.model, _id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            await self.db.commit()
            await self.db.refresh(instance)
        return instance

    async def delete(self, _id: int):
        stmt = sa.delete(self.model).where(sa.col(self.model.id) == _id)
        await self.db.execute(stmt)

    async def delete_with_clauses(self, clauses):
        stmt = sa.delete(self.model).where(*clauses)
        await self.db.execute(stmt)

    async def get_many_by_ids(self, ids: Iterable[int]) -> Sequence[ModelType]:
        clauses = [sa.col(self.model.id).in_(ids)]
        return await self.get_all(clauses)

    async def vf_ids(self, ids: Iterable[int]) -> bool:
        items = await self.get_many_by_ids(ids)
        existed_ids = set([item.id for item in items])
        if not (existed_ids >= set(ids)):
            return False
        return True

    async def vf_id(self, _id: int) -> bool:
        item = await self.get_by_id(_id)
        if item is None:
            raise False
        return True
