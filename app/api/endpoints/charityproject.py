from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_project_exists
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate

router = APIRouter()


@router.get('/', response_model=list[CharityProjectDB],
            response_model_exclude_none=True)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Эндпоинт для получения всех проектов."""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post('/', response_model=CharityProjectDB, response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)])
async def create_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Эндпоинт для создания проектов (только суперюзер)."""
    new_project = await charity_project_crud.create_project(
        project, session
    )
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Эндпоинт для обновления данных проекта (только суперюзер)."""
    project = await check_project_exists(
        project_id, session
    )
    project = await charity_project_crud.update(
        project, obj_in, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Эндпоинт для удаления проектов (только суперюзер)."""
    project = await check_project_exists(
        project_id, session
    )
    project = await charity_project_crud.remove(
        project, session
    )
    return project
