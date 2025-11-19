#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Add a user to the db """
        session = self._session
        user = User(email=email, hashed_password=hashed_password)
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ Find a user """
        user_keys = []
        for column in User.__table__.columns.keys():
            user_keys.append(column)

        invalid = set(kwargs.keys()) - set(user_keys)
        if invalid:
            raise InvalidRequestError

        session = self._session
        arg = list(kwargs.keys())
        first_arg = arg[0]
        user_found = (
            session.query(User)
            .filter_by(**{first_arg: kwargs[first_arg]})
            .first()
        )
        if not user_found:
            raise NoResultFound

        return user_found

    def update_user(self, user_id: int, **kwargs):
        """ Update the user """
        user_keys = []
        for column in User.__table__.columns.keys():
            user_keys.append(column)

        invalid = set(kwargs.keys()) - set(user_keys)
        if invalid:
            raise ValueError

        user = self.find_user_by(id=user_id)
        if not user:
            raise ValueError

        args = list(kwargs.keys())
        for arg in args:
            setattr(user, arg, kwargs[arg])

        session = self._session
        session.commit()
