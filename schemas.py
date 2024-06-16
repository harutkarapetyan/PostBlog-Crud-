# For Data Validations
from pydantic import BaseModel, EmailStr


class UserAdd(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    name: str
    email: EmailStr
    # main_photo: bytes


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class CreatePost(BaseModel):
    title: str
    content: str


class UpdatePost(BaseModel):
    title: str
    content: str


class CreateComment(BaseModel):
    text: str


class UpdateComment(BaseModel):
    text: str


class UpdateSettings(BaseModel):
    language: str
    background_color: str
    font_size: int


class PasswordReset(BaseModel):
    new_password: str
    mail: str
    confirm_password: str


