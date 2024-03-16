from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.services import close_object_after_check_invested_amount


class CRUDBase:
    """Базовый CRUD-класс для CharityProject и Donation."""

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        """Метод для получения объекта по его id."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        """Метод для получения всех объектов."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
            commit: Optional[bool] = True
    ):
        """Метод для создания объекта."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        """Метод для обновления данных объекта."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj = close_object_after_check_invested_amount(db_obj)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        """Метод для удаления объекта."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_open_objects(
        self,
        open_model,
        session: AsyncSession
    ):
        """Метод для получения всех открытых объектов указанной модели."""
        open_objs = await session.execute(
            select(open_model).where(
                open_model.fully_invested == false()
            )
        )
        return open_objs.scalars().all()
