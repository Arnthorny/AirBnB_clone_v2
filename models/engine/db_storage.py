#!/usr/bin/python3
"""Defines a DBStorage class"""
import os
from models.city import City
from models.user import User
from models.place import Place, place_amenity
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


MODELS = [City, User, Place, State, Review, Amenity]

HBNB_ENV = os.getenv("HBNB_ENV")
HBNB_MYSQL_USER = os.getenv("HBNB_MYSQL_USER")
HBNB_MYSQL_PWD = os.getenv("HBNB_MYSQL_PWD")
HBNB_MYSQL_HOST = os.getenv("HBNB_MYSQL_HOST")
HBNB_MYSQL_DB = os.getenv("HBNB_MYSQL_DB")


class DBStorage:
    """Represents a database storage engine"""

    __engine = None
    __session = None

    def __init__(self):
        """Initializes the class"""
        url = "mysql+mysqldb://{}:{}@{}/{}".format(
                HBNB_MYSQL_USER,
                HBNB_MYSQL_PWD,
                HBNB_MYSQL_HOST,
                HBNB_MYSQL_DB)
        self.__engine = create_engine(url, pool_pre_ping=True)

        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries current database session"""
        objects = {}
        if cls:
            if type(cls) == str:
                cls = eval(cls)
            query = self.__session.query(cls).all()
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            for model in MODELS:
                query = self.__session.query(model).all()
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """"Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and
        create the current database session"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()

    def close(self):
        """
        Closes a current session
        """
        self.__session.close()
