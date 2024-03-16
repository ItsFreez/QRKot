from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

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

    __table_args__ = (
        CheckConstraint(
            f'full_amount >= {MIN_FULL_AMOUNT}',
            name='check_full_amount_positive'
        ),
        CheckConstraint(
            'full_amount >= invested_amount',
            name='check_full_not_less_invested'
        ),
    )
