#!/usr/bin/python3
""" DBStorage module for the HBNB project """
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ Database storage class """

    __engine = None
    __session = None

    def __init__(self):
        """ Initialize the database storage """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(getenv("HBNB_MYSQL_USER"),
                                              getenv("HBNB_MYSQL_PWD"),
                                              getenv("HBNB_MYSQL_HOST"),
                                              getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query objects based on class name """
        objects = {}
        classes = [State, City, User, Place, Review, Amenity]

        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self.__session.query(cls)
        else:
            query = self.__session.query(*classes)

        for obj in query:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            objects[key] = obj
        return objects

    def new(self, obj):
        """ Add the object to the current database session """
        if obj:
            self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the db and create the current db session """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """ Close the session """
        self.__session.close()
