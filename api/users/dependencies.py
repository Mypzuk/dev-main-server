from fastapi.params import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from .errors import ErrorTemplates
from . import functions as func

from core.db_helper import db_helper
from .schemas import UserCreate, UserCheck


async def check_user_id(user_id: int, session: AsyncSession = Depends(db_helper.session_getter)):
    user = await func.get_user(session=session, id=user_id)
    if not user:
        return ErrorTemplates.not_found()
    return user


async def check_user_phone(user_in: UserCreate, session: AsyncSession = Depends(db_helper.session_getter)):
    user = await func.get_user(session=session, phone=user_in.phone)
    if user is not None:
        return ErrorTemplates.user_already_exists()
    return user_in