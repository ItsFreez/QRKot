from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.orm import validates

from app.core.constants import DEFAULT_INV_AMOUNT, MIN_FULL_AMOUNT
from app.core.db import Base


class ProjectDonationAbstractModel(Base):
    """Абстрактная модель для CharityProject и Donation."""

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=DEFAULT_INV_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime)

    @validates('full_amount')
    def validate_full_amount(self, key, value):
        if value < MIN_FULL_AMOUNT:
            raise ValueError('Значение должно быть больше 0!')
        return value
