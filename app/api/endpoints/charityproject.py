from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_actuallity_project, check_invested_amounts,
    check_name_duplicate, check_project_exists
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.models import Donation
from app.schemas import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
from app.services import investment

router = APIRouter()


@router.get('/', summary='Получить список всех проектов',
            response_model=list[CharityProjectDB], response_model_exclude_none=True)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Эндпоинт для получения всех проектов."""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post('/', summary='Создать проект (суперюзер)',
             response_model=CharityProjectDB, response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)])
async def create_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Эндпоинт для создания проектов (только суперюзер)."""
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(
        project, session, commit=False
    )
    open_objs = await charity_project_crud.get_open_objects(
        Donation, session
    )
    if open_objs:
        changed_objs = investment(new_project, open_objs)
        for obj in changed_objs:
            session.add(obj)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    summary='Обновить данные существующего проекта',
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
    await check_invested_amounts(
        project, obj_in_data
    )
    project = await charity_project_crud.update(
        project, obj_in, session
    )
    return project


@router.delete(
    '/{project_id}',
    summary='Удалить существующий проект',
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
    project = await charity_project_crud.remove(
        project, session
    )
    return project
