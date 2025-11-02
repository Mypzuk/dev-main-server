from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from . import functions as func
from .errors import ErrorTemplates
from .schemas import ResultCreate, ResultDenied

from api.competitions.dependencies import check_competition_id
from api.users.dependencies import check_user_id


async def check_result_id(result_id: int, session: AsyncSession = Depends(db_helper.session_getter)):
    result = await func.get_result(session=session, result_id=result_id)
    if not result:
        return ErrorTemplates.not_found()
    return result


async def check_user_competition(result_in: ResultCreate | ResultDenied, session: AsyncSession = Depends(db_helper.session_getter)):
    # result = await check_result_id(result_id=result_in.id, session=session)
    competition = await check_competition_id(competition_id=result_in.competition_id, session=session)
    user = await check_user_id(user_id=result_in.user_id, session=session)
    return result_in