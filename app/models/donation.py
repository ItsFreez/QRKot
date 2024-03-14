from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.common import ProjectDonationAbstractModel


class Donation(ProjectDonationAbstractModel):
    """Модель пожертвований."""

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)