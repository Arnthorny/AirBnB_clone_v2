#!/usr/bin/python3
"""Defines a User class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Represents a user"""

    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    places = relationship(
            'Place',
            backref="user",
            cascade="all, delete-orphan")
    reviews = relationship(
            "Review",
            backref="user",
            cascade="all, delete-orphan")

    @property
    def places(self):
        """Gets the attribute"""
        places = models.storage.all("Place").values()
        return [place for place in places if place.user_id == self.id]

    @property
    def reviews(self):
        """Gets the attribute"""
        reviews = models.storage.all("Review").values()
        return [review for review in reviews if review.user_id == self.id]
