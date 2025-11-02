from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from . import dependencies
from core.db_helper import db_helper

from . import functions as func
from .schemas import Competition, CompetitionCreate

router = APIRouter(tags=["Сompetitions 🚀"])


@router.get("/competitions/current")
async def get_current_competitions(session: AsyncSession = Depends(db_helper.session_getter)):
    return await func.get_current_competitions(session=session)

@router.get("/competitions/{competition_id}")
async def get_competition(competition: Competition = Depends(dependencies.check_competition_id)):
    return competition
    
@router.get("/competitions")
async def get_competitions(session: AsyncSession = Depends(db_helper.session_getter)):
    return await func.get_competitions(session)

@router.post("/competitions")
async def create_competition(competition_in: CompetitionCreate, session: AsyncSession = Depends(db_helper.session_getter)):
    return await func.create_competition(session=session, competition_in=competition_in)

@router.put("/competitions/{competition_id}")
async def update_competition(competition_in: CompetitionCreate, competition: Competition = Depends(dependencies.check_competition_id), session: AsyncSession = Depends(db_helper.session_getter)):
    return await func.update_competition(competition_in=competition_in, competition=competition, session=session)


@router.delete("/competitions/{competition_id}")
async def delete_competition(competition_in: Competition = Depends(dependencies.check_competition_id), session: AsyncSession = Depends(db_helper.session_getter)):
    return await func.delete_competition(competition_in=competition_in, session=session)


