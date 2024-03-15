from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Функция проверяет уникальность имени проекта."""
    project = await charity_project_crud.get_project_by_name(project_name, session)
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Функция выполняет проверку, что объект существует."""
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


async def check_amount_not_less_invested(
        project: CharityProject,
        obj_in: CharityProjectUpdate
) -> None:
    """Функция выполняет проверку, что новая сумма не меньше, чем уже инвестированная."""
    obj_in_data = obj_in.dict()
    new_full_amount = obj_in_data.get('full_amount')
    if new_full_amount is not None and project.invested_amount > new_full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нелья установить значение full_amount меньше уже вложенной суммы.'
        )
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нелья изменять закрытый проект.'
        )


async def check_actuallity_project(project: CharityProject) -> None:
    """Функция проверяет инвестировались ли уже деньги в проект."""
    if project.fully_invested or project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
