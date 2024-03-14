from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas import CharityProjectCreate


class CRUDCharityProject(CRUDBase):

    async def get_project_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        db_project = await session.execute(
            select(CharityProject).where(
                CharityProject.name == project_name
            )
        )
        db_project = db_project.scalars().first()
        return db_project

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
