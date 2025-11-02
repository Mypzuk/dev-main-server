from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession



from . import dependencies
from .schemas import User, UserCreate, UserUpdate
from core.db_helper import db_helper

from . import functions as func

router = APIRouter(tags=["Users 👥"])


@router.get("/user/{user_id}")
async def get_user(user: User = Depends(dependencies.check_user_id)):
    return user


@router.get("/users")
async def get_users(session: AsyncSession = Depends(db_helper.session_getter)):
    return await func.get_users(session=session)


@router.post("/users")
async def create_user(user_in: UserCreate = Depends(dependencies.check_user_phone), session: AsyncSession = Depends(db_helper.session_getter)):
    return await func.create_user(session=session, user_in=user_in)


@router.put("/users/{user_id}")
async def update_user(user_in: UserCreate, user = Depends(dependencies.check_user_id), session: AsyncSession = Depends(db_helper.session_getter)):
    return await func.update_user(session=session, user_in=user_in, user=user)

@router.delete("/users/{user_id}")
async def delete_user(user_in: User = Depends(dependencies.check_user_id), session: AsyncSession = Depends(db_helper.session_getter)):
    return await func.delete_user(session=session, user_in=user_in)

@router.get("/users/{user_id}/profile")
async def get_user_profile(user: User = Depends(dependencies.check_user_id), session: AsyncSession = Depends(db_helper.session_getter)):
    return await func.get_user_profile(user=user, session=session)



@router.patch('/users/{user_id}/params')
async def update_user_params(user_in: UserUpdate, user = Depends(dependencies.check_user_id), session: AsyncSession = Depends(db_helper.session_getter)):
    return await func.patch_user(session=session, user_in=user_in, user=user)