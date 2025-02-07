import sqlalchemy as sa
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Generic, Sequence, Iterable, Type
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi_share_core.db import AsyncSessionDep
from fastapi_share_core.meta.db_service import DALMeta

ModelType = TypeVar("ModelType")


class DAL(Generic[ModelType], metaclass=DALMeta):
    model: ModelType

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, _id: int) -> ModelType | None:
        stmt = sa.select(self.model).where(self.model.id == _id)
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
        stmt = sa.delete(self.model).where(self.model.id == _id)
        await self.db.execute(stmt)

    async def delete_with_clauses(self, clauses):
        stmt = sa.delete(self.model).where(*clauses)
        await self.db.execute(stmt)

    async def get_many_by_ids(self, ids: Iterable[int]) -> Sequence[ModelType]:
        clauses = [self.model.id.in_(ids)]
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


def dal_maker_factory(dal_type: Type[DAL]):
    def dal_maker(db: AsyncSessionDep):
        executor = dal_type(db=db)
        logger.debug(f"新建db会话: {id(db)}")
        logger.debug(f"新建DbServiceExecutor: {id(executor)}")
        return executor

    return dal_maker
