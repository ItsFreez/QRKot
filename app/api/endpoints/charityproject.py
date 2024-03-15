from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_actuallity_project, check_amount_not_less_invested,
    check_name_duplicate, check_project_exists
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.models import Donation
from app.schemas import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
from app.services import investment

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
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(
        project, session
    )
    new_project = await investment(
        new_project, Donation, session
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
    obj_in_data = obj_in.dict()
    if obj_in_data.get('name') is not None:
        await check_name_duplicate(obj_in_data['name'], session)
    await check_amount_not_less_invested(
        project, obj_in
    )
    project = await charity_project_crud.update_project(
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
    await check_actuallity_project(project)
    project = await charity_project_crud.remove_project(
        project, session
    )
    return project
