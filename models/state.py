#!/usr/bin/python3
"""Defines a State class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """Represents a state"""

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship(
            'City',
            backref="state",
            cascade="all, delete-orphan")

    @property
    def cities(self):
        """Gets the attribute"""
        cities = models.storage.all("City")
        return [city for city in cities if city.state_id == self.id]
        
