from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationCreate(BaseModel):
    """Pydantic-схема для создания пожертвования."""

    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'full_amount': 10,
                'comment': 'На корм бедным пушистикам.',
            }
        }


class DonationDBForUsers(DonationCreate):
    """Pydantic-схема для чтения пожертвования пользователями."""

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBForSuperUser(DonationDBForUsers):
    """Pydantic-схема для чтения пожертвования супер-пользователем."""

    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
