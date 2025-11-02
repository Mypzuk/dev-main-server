from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import functions as func
from . import dependencies
from core.db_helper import db_helper

from api.competitions.dependencies import check_competition_id

from api.competitions.schemas import CompetitionCreate
from .schemas import Result, ResultCreate, ResultDenied

router = APIRouter(tags=["Results 🎯"])



@router.get("/results/{result_id}")
async def get_result(result: Result = Depends(dependencies.check_result_id)):
    return result
@router.get("/results")
async def get_results(session: AsyncSession = Depends(db_helper.session_getter)):
    return await func.get_results(session=session)



@router.post("/results")
async def create_result(
        result_in: ResultCreate = Depends(dependencies.check_user_competition),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    return await func.create_result(result_in=result_in, session=session)


@router.put("/results/{result_id}")
async def update_result(
        result_in: ResultCreate = Depends(dependencies.check_user_competition),
        result: Result = Depends(dependencies.check_result_id),
        session: AsyncSession = Depends(db_helper.session_getter)):
    return await func.update_result(result_in=result_in, result=result, session=session)



@router.delete("/results/{result_id}")
async def delete_result(
        result_in: Result = Depends(dependencies.check_result_id),
        session: AsyncSession = Depends(db_helper.session_getter)
                        ):
    return await func.delete_result(result_in=result_in, session=session)


@router.get("/results/{user_id}/info")
async def user_results_info(user_id: int = Depends(dependencies.check_user_id),
                            session: AsyncSession = Depends(db_helper.session_getter)):
    return await func.user_results_info(user_id=user_id, session=session)


@router.get("/results/{competition_id}/leaderboard")
async def leaderboard(competition_id: CompetitionCreate = Depends(dependencies.check_competition_id),
                            session: AsyncSession = Depends(db_helper.session_getter)):
    return await func.leaderboard(competition_id=competition_id, session=session)


@router.post("/results/denied-result")
async def denied_result(
        result_in: ResultDenied = Depends(dependencies.check_user_competition),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    return await func.denied_result(result_in=result_in, session=session)