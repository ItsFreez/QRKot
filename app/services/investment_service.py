from datetime import datetime
from typing import Union

from app.core.constants import DEFAULT_INV_AMOUNT
from app.models import CharityProject, Donation


def close_object_after_check_invested_amount(
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


def investment(
        target: Union[CharityProject, Donation],
        sources: list[Union[CharityProject, Donation]]
) -> list[Union[CharityProject, Donation]]:
    """
    Функция производит расчет инвестиций между проектами и пожертвованиями
    и вызывает закрытие проекта/пожертвования, если был достигнут лимит.
    """
    target.invested_amount = DEFAULT_INV_AMOUNT
    changed_objs = []
    for open_obj in sources:
        amount_to_close_open = min(
            (target.full_amount - target.invested_amount,
             open_obj.full_amount - open_obj.invested_amount)
        )
        for obj in (target, open_obj):
            obj.invested_amount += amount_to_close_open
            obj = close_object_after_check_invested_amount(obj)
        changed_objs.append(open_obj)
        if target.fully_invested:
            break
    return changed_objs
