#!/usr/bin/env python3
"""
The User model module
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)
    hashed_password = Column(String(250), nullable=False, unique=True)
    session_id = Column(String(250), nullable=True, unique=True)
    reset_token = Column(String(250), nullable=True)
