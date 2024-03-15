from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject


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


async def check_invested_amounts(
        project: CharityProject,
        obj_in_data: dict
) -> None:
    """
    Функция выполняет проверку, что проект не закрыт и новая сумма
    не меньше, чем уже инвестированная.
    """
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя изменять закрытый проект.'
        )
    new_full_amount = obj_in_data.get('full_amount')
    if new_full_amount is not None and project.invested_amount > new_full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить значение full_amount меньше уже вложенной суммы.'
        )


async def check_actuallity_project(project: CharityProject) -> None:
    """Функция проверяет инвестировались ли уже деньги в проект."""
    if project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
