
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .errors import ErrorTemplates
from api.responses import ResponseTemplates
from .schemas import UserSchemas

from core.models import Users, Results

from typing import Optional



# **kwargs позволяет искать пользователя не только по id, но и по другим параметрам. !ВАЖНО! чтоб искомый параметр был в БД!
async def get_user(session: AsyncSession, **kwargs):
    query = select(Users)
    for key, value in kwargs.items():
        query = query.where(getattr(Users, key) == value)
    result = await session.execute(query)
    user = result.scalars().first()
    return user

async def get_users(session: AsyncSession):
    stmt = select(Users).order_by(Users.id)
    result = await session.execute(stmt)
    users = result.scalars().all()
    users_schemas = [UserSchemas.model_validate(user) for user in users]
    return ResponseTemplates.success(data=users_schemas)

async def create_user(session: AsyncSession, user_in, token: Optional[str] = None):
    user = Users(**user_in.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    if token:
     return ResponseTemplates.success(data={"user_id":user.id, "token": token}, message="User created successfully")
    return ResponseTemplates.success(data={"user_id":user.id}, message="User created successfully")
 

async def update_user(session: AsyncSession, user_in, user):
    for name, value in user_in:
        setattr(user, name, value)
    await session.commit()
    return ResponseTemplates.success(user_in)

async def delete_user(session: AsyncSession, user_in):
    await session.delete(user_in)
    await session.commit()
    return ResponseTemplates.success(message=f"User deleted")


async def get_user_profile(user, session: AsyncSession):

    
    tournaments_stmt = (
        select(func.count(func.distinct(Results.competition_id)))
        .where(Results.user_id == user.id)
    )
    result = await session.execute(tournaments_stmt)
    tournaments_count = result.scalar() or 0
    
    
    if not user:
        return ErrorTemplates.not_found()
    return ResponseTemplates.success(data={
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "level": "1", 
        "current_experience": user.current_experience,
        "rank": "Новичок", 
        "tournaments": tournaments_count

    })
    



async def patch_user(session, user_in, user):
    for name, value in user_in:
        setattr(user, name, value)
    await session.commit()
    return ResponseTemplates.success(user_in)
    