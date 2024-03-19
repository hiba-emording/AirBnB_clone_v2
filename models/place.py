#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from models.review import Review
from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


metadata = Base.metadata

place_amenity = Table('place_amenity', metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True,
                             nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    user = relationship("User", back_populates="places")
    city = relationship("City", back_populates="places")

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
                "Review",
                cascade="all, delete",
                back_populates="place"
                )
        amenities = relationship(
                "Amenity",
                secondary='place_amenity',
                viewonly=False
                )

    else:
        @property
        def reviews(self):
            """Get list of all linked Reviews"""
            return [review for review in models.storage.all().values()
                    if isinstance(review, Review)
                    and review.place_id == self.id]

        amenity_ids = []

        @property
        def amenities(self):
            """Getter to return list of Amenity instances"""
            return [storage.get("Amenity", amenity_id)
                    for amenity_id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Setter to handle append method for adding an Amenity.id"""
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
