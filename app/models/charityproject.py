from sqlalchemy import Column, String, Text

from app.core.constants import MAX_LEN_NAME
from app.models.common import ProjectDonationAbstractModel


class CharityProject(ProjectDonationAbstractModel):
    """Модель проектов для пожертвования."""

    name = Column(String(MAX_LEN_NAME), unique=True, nullable=False)
    description = Column(Text, nullable=False)
