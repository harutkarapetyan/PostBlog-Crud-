from sqlalchemy import Column, Integer, String, text, ForeignKey, Float, ARRAY, LargeBinary, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP

from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))
    profile_photo = Column(String, nullable=True)
    status = Column(Boolean, nullable=False, server_default="False")


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("users.user_id"))


class Like(Base):
    __tablename__ = "likes"
    like_id = Column(Integer, nullable=False, primary_key=True)
    likes_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))

    post_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)


class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, nullable=False, primary_key=True)
    comment_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))
    post_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    text = Column(String, nullable=False)


class UserSetting(Base):
    __tablename__ = "user_settings"

    setting_id = Column(Integer, nullable=False, primary_key=True)
    language = Column(String, nullable=False, server_default="en")
    background_color = Column(String, nullable=False, server_default="white")
    font_size = Column(Float, nullable=False, server_default="12.0")

    user_id = Column(Integer, nullable=False)


class PossibleSetting(Base):
    __tablename__ = "possible_settings"

    id = Column(Integer, nullable=False, primary_key=True)
    possible_languages = Column(ARRAY(String), nullable=False)
    possible_background_colors = Column(ARRAY(String), nullable=False)
    possible_settings_font_size = Column(Float, nullable=False)


class Images(Base):
    __tablename__ = "users_images"

    id = Column(Integer, nullable=False, primary_key=True)
    image = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))
    user_id = Column(Integer, nullable=False)


# class Message(Base):
#     __tablename__ = "message"


