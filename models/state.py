#!/usr/bin/python3
""" State Module for HBNB project """

# Import necessary modules and classes
import models
from models.base_model import BaseModel, Base
from models.city import City
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    # Define the name of the table in the database
    __tablename__ = "states"

    # Define a column for the state's name, which cannot be empty
    name = Column(String(128), nullable=False)

    # Establish a one-to-many relationship with the City class
    cities = relationship("City", backref="state")

    def __init__(self, *args, **kwargs):
        """
        Constructor method for State class, inheriting from BaseModel.
        Initializes object attributes with given arguments.
        """
        super().__init__(*args, **kwargs)

    if models.storage_type != "db":
        @property
        def cities(self):
            """Getter method for cities that returns a list of City instances
            associated with the current State instance.
            """
            list_city = []
            all_inst_c = models.storage.all(City)
            for value in all_inst_c.values():
                if value.state_id == self.id:
                    list_city.append(value)
            return list_city
