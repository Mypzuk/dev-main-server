from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    id: int
    

class UserCheck(BaseModel): 
    phone: str

class UserLogin(BaseModel):
    phone: str
    code:str


class UserRegister(BaseModel):
    phone: str
    first_name: str
    last_name: str
    birth_date: date
    sex: str = "M"

class UserProfile(User):
  
    last_name: str | None = None
    birth_date: date | None = None
    sex: str = "M"
    

class UserUpdate(BaseModel): 
    first_name: str
    last_name: str 
    weight: float | None
    height: float | None

class UserCreate(BaseModel):
    phone: str
    telegram_id: str | None = None
    telegram_link: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    birth_date: date | None = None
    sex: str | None = None
    weight: float | None = None
    height: float | None = None

class UserSchemas(UserCreate):
    id: int
    total_experience: float | None = None
    current_experience: float | None = None
    class Config:
        from_attributes = True