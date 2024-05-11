from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String, Float, )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.db.utils import CustomBaseModel

Base = declarative_base(cls=CustomBaseModel)


class Users(Base):
    __tablename__ = "user_info"

    user_id = Column(
        Integer,
        primary_key=True,
        unique=True,
    )
    email_id = Column(String, unique=True, nullable=False)
    # user_type = Column(String, nullable=True)
    name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    logout = Column(Boolean, nullable=False)
    videos = relationship("VideoInfo", back_populates="owner")


class VideoInfo(Base):
    __tablename__ = "video_information"

    video_id = Column(
        String,
        primary_key=True,
        unique=True,
    )
    title = Column(String, nullable=True)
    description = Column(String)
    duration = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow)
    resolution = Column(String)
    format = Column(String)
    filename = Column(String, nullable=False)
    thumbnail_filename = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("user_info.user_id"))  # ForeignKey relationship with User table
    owner = relationship("Users", back_populates="videos")  # Define relationship with User model
