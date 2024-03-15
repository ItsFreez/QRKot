from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.core.constants import MAX_LEN_NAME, MIN_LEN_NAME, MIN_FULL_AMOUNT


class CharityProjectBase(BaseModel):
    """Базовая Pydantic-схема для проектов с основными настройками."""

    name: Optional[str] = Field(None, min_length=MIN_LEN_NAME, max_length=MAX_LEN_NAME)
    description: Optional[str] = Field(None, min_length=MIN_FULL_AMOUNT)
    full_amount: Optional[PositiveInt]

    @staticmethod
    def value_cannot_be_null(key, value):
        if value is None:
            raise ValueError(f'Поле {key} не может быть пустым!')
        return value

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': 'На корм пушистикам',
                'description': 'Проект собирает деньги на помощь котикам, которым нечего кушать',
                'full_amount': 10
            }
        }


class CharityProjectCreate(CharityProjectBase):
    """Pydantic-схема для создания проекта."""

    name: str = Field(..., min_length=MIN_LEN_NAME, max_length=MAX_LEN_NAME)
    description: str = Field(..., min_length=MIN_FULL_AMOUNT)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    """Pydantic-схема для обновления проекта."""

    @validator('name')
    def name_cannot_be_null(cls, value):
        return cls.value_cannot_be_null('name', value)

    @validator('description')
    def description_cannot_be_null(cls, value):
        return cls.value_cannot_be_null('description', value)

    @validator('full_amount')
    def full_amount_cannot_be_null(cls, value):
        return cls.value_cannot_be_null('full_amount', value)


class CharityProjectDB(CharityProjectCreate):
    """Pydantic-схема для чтения проекта."""

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
