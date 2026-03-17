#!/usr/bin/python3
"""Place model"""

import uuid
from datetime import datetime
from app import db
from app.models.user import User
from app.models.amenity import Amenity

class Place(db.Model):
    """SQLAlchemy model for Place"""

    __tablename__ = 'places'
    all_places = {}

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, title, description, price, latitude, longitude, owner):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # Validation
        if not title or len(title) > 100:
            raise ValueError("Title is required and must be <= 100 characters")

        if price <= 0:
            raise ValueError("Price must be a positive number")

        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90 and 90")

        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180 and 180")

        if not isinstance(owner, User):
            raise ValueError("Owner must be a User instance")

        # Assign attributes
        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner = owner
        self.owner_id = owner.id

        self.reviews = []
        self.amenities = []

        # Register in the global dictionary
        Place.all_places[self.id] = self

    # Add a review
    def add_review(self, review):
        from app.models.review import Review
        if not isinstance(review, Review):
            raise ValueError("Invalid review")
        self.reviews.append(review)
        self.save()

    # Add an amenity
    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise ValueError("Invalid amenity")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    # Update timestamps
    def save(self):
        self.updated_at = datetime.now()

    # Update attributes from a dict
    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

# Helper function for other endpoints
def get_place_by_id(place_id):
    return Place.all_places.get(place_id)

