from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    user_name: str
    user_email: EmailStr
    password: str

class UserLogin(BaseModel):
    user_email: EmailStr
    password: str

class NoteBase(BaseModel):
    note_title: str
    note_content: str

class NoteOut(NoteBase):
    note_id: str
    created_on: datetime

    class Config:
        orm_mode = True

