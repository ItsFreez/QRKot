from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_donations_for_owner(
            self,
            user: User,
            session: AsyncSession
    ) -> list[Donation]:
        """Метод для получения всех объектов пожертвования для их владельца."""
        db_objs = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )
        return db_objs.scalars().all()


donation_crud = CRUDDonation(Donation)
