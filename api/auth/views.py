from fastapi import APIRouter, Request, Depends
from . import functions as func
from core.db_helper import db_helper
from fastapi.security import OAuth2PasswordBearer

from api.users.schemas import UserCheck





oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")



from api.users.schemas import UserLogin, UserRegister 

router = APIRouter(tags=["Auth 🔒"])

@router.post("/verify-code")
async def verify_code(user_in: UserLogin, session = Depends(db_helper.session_getter)):
    return await func.verify_code(user_in=user_in, session=session)



@router.post("/register")
async def register(user: UserRegister, session = Depends(db_helper.session_getter)):
    return await func.register(user, session)


@router.post("/check_user")
async def check_user(user: UserCheck, session = Depends(db_helper.session_getter)):
    return await func.check_user(user = user, session = session)

@router.get('/me')
async def me(token: str = Depends(oauth2_scheme), session = Depends(db_helper.session_getter)):
    return await func.me(token=token, session=session)