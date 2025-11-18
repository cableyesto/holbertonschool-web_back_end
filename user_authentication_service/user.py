#!/usr/bin/env python3
"""
User model file
"""
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """ User Model Class """
    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        """ String representation User object """
        return (
            "<User(id={}, email='{}', session_id='{}', reset_token='{}')>"
            .format(
                self.id,
                self.email,
                self.session_id,
                self.reset_token
            )
        )
