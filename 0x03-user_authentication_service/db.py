#!/usr/bin/env python3
"""
DB Module
"""

from typing import TypeVar
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base
from user import User


class DB:
    """DB Class"""

    def __init__(self) -> None:
        """Initializes a new database instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized Session Object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Creates a New User instance
        And Adds it to the db

        Returns created instance
        Args:
            email (str): User Email
            hashed_password (str): User Password

        Returns:
            User: Created User Instance
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds usr using given kwargs
        Raises:
            InvalidRequestError: Raised when wrong query arguments are passed
            NoResultFound: Raised If no user were found

        Returns:
            User: User Instance
        """
        try:
            usr = self._session.query(User).filter_by(**kwargs).first()
        except InvalidRequestError:
            raise InvalidRequestError()
        if not usr:
            raise NoResultFound()
        return usr

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates User Instance
        Args:
            user_id (int): User ID
            Used to retrieve usr object from db

        Raises:
            ValueError: raised when a given query argument
            is not defined in usr columns

        Returns:
            None
        """
        usr = self.find_user_by(id=user_id)
        if usr:
            valid_columns = {column.name for column in usr.__table__.columns}
            for k, v in kwargs.items():
                if k in valid_columns:
                    setattr(usr, k, v)
                else:
                    raise ValueError()
            self._session.commit()
        return None
