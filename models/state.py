#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'  # Table name for SQLAlchemy

    name = Column(String(128), nullable=False)

    # For DBStorage: Establish a one-to-many relationship with City
    # If the State object is deleted, all linked objects are deleted.
    cities = relationship('City', backref='state',
                          cascade='all, delete-orphan', passive_deletes=True)

    # For FileStorage: Create a getter attribute to return City state_id
    @property
    def cities(self):
        from models import storage
        all_cities = storage.all("City")
        return [city for city in all_cities.values()
                if city.state_id == self.id]
