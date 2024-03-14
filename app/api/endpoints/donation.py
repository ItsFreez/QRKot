from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud import donation_crud
from app.models import User
from app.schemas import DonationCreate, DonationDBForSuperUser, DonationDBForUsers

router = APIRouter()


@router.get('/', response_model=list[DonationDBForSuperUser],
            response_model_exclude_none=True,
            dependencies=[Depends(current_superuser)])
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Эндпоинт для получения всех пожертвований (только суперюзер)."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post('/', response_model=DonationDBForUsers, response_model_exclude_none=True)
async def create_reservation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Эндпоинт для создания пожертвований."""
    new_donation = await donation_crud.create_donation(
        donation, session, user
    )
    return new_donation


@router.get('/my', response_model=list[DonationDBForUsers],
            response_model_exclude_none=True)
async def get_owner_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Эндпоинт для получения всех пожертвований текущего пользователя."""
    all_owner_donations = await donation_crud.get_donations_for_owner(user, session)
    return all_owner_donations
