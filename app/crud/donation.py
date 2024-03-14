from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_donations_for_owner(
            self,
            user: User,
            session: AsyncSession
    ):
        """Метод для получения всех объектов пожертвования для их владельца."""
        db_objs = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )
        return db_objs.scalars().all()

    async def create_donation(
            self,
            obj_in,
            session: AsyncSession,
            user: User
    ):
        """Метод для создания пожертвования."""
        obj_in_data = obj_in.dict()
        obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


donation_crud = CRUDDonation(Donation)
