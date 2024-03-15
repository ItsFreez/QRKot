from datetime import datetime
from typing import Union

from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


def check_and_close_object(
        obj: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    """
    Функция проверяет достигнута ли требуемая сумма инвестиций и,
    при необходимости, закрывает проект/пожертвование.
    """
    if obj.full_amount == obj.invested_amount:
        obj.fully_invested = True
        obj.close_date = datetime.utcnow()
    return obj


def investment_counter(
    new_obj: Union[CharityProject, Donation],
    open_obj: Union[CharityProject, Donation],
) -> tuple[Union[CharityProject, Donation], Union[CharityProject, Donation]]:
    """Производит расчет инвестиций между проектами и пожертвованиями."""
    amount_to_close_new = new_obj.full_amount - new_obj.invested_amount
    amount_to_close_open = open_obj.full_amount - open_obj.invested_amount
    if amount_to_close_new <= amount_to_close_open:
        open_obj.invested_amount += amount_to_close_new
        new_obj.invested_amount += amount_to_close_new
    else:
        open_obj.invested_amount += amount_to_close_open
        new_obj.invested_amount += amount_to_close_open
    return new_obj, open_obj


async def investment(
        new_obj: Union[CharityProject, Donation],
        open_model: Union[CharityProject, Donation],
        session: AsyncSession
) -> Union[CharityProject, Donation]:
    """
    Функция выполняет поиск открытых проектов/пожертвований и
    запускает процесс инвестиций и закрытия проектов/пожертвований.
    """
    open_objs = await session.execute(
        select(open_model).where(
            open_model.fully_invested == false()
        )
    )
    open_objs = open_objs.scalars().all()
    for open_obj in open_objs:
        new_obj, open_obj = investment_counter(new_obj, open_obj)
        open_obj = check_and_close_object(open_obj)
        session.add(open_obj)
        new_obj = check_and_close_object(new_obj)
        if new_obj.fully_invested:
            break
    session.add(new_obj)
    await session.commit()
    await session.refresh(new_obj)
    return new_obj
