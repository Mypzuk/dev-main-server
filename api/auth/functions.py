from api.users.functions import get_user, create_user
from api.users.errors import ErrorTemplates
from api.users.functions import get_user

from api.responses import ResponseTemplates

from .utils import create_token, decode_jwt_token


async def verify_code(user_in, session):
    print(user_in)
    user = await get_user(session=session, phone=user_in.phone)
    if not user:
        return ErrorTemplates.not_found()
    if user_in.code != "11111":
        return ErrorTemplates.invalid_code()
    token = await create_token({"phone":user_in.phone})
    return {"user_id": user.id, "token": token}



async def register(user, session):
    print(user)
    user_check = await get_user(session=session, phone=user.phone)
    if user_check:
        return ErrorTemplates.user_already_exists()
    token = await create_token({"phone":user.phone})
    return await create_user(session=session, user_in=user, token=token)



async def check_user(user, session): 
    print(user)
    user = await get_user(session=session, phone=user.phone)
    if user:
        token = await create_token({'phone':user.phone})
        return ResponseTemplates.success(data={"isRegistered": "true", "user_id": user.id, "token":token})
    return ResponseTemplates.success(data={"isRegistered": "false"})
    

async def me(token, session):
   phone =  await decode_jwt_token(token)
   user = await get_user(session=session, phone=phone)
   if user is None: 
       return ErrorTemplates.not_found
   token = await create_token({"phone": phone})
   return {"user_id": user.id, "token": token}