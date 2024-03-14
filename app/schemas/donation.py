from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

from pydantic import BaseModel, Extra, Field

from app.core.constants import NOT_VALID_AMOUNT


class DonationBaseCreate(BaseModel):
    """Pydantic-схема для создания пожертвования."""

    full_amount: Annotated[int, Field(strict=True, gt=NOT_VALID_AMOUNT)]
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationDBForUsers(DonationBaseCreate):
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
