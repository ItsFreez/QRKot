from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas import CharityProjectCreate


class CRUDCharityProject(CRUDBase):

    async def create_project(
            self,
            obj_in: CharityProjectCreate,
            session: AsyncSession,
    ) -> CharityProject:
        """Метод для создания проекта."""
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


charity_project_crud = CRUDCharityProject(CharityProject)
