#!/usr/bin/python3
"""Review Model"""

import uuid
from datetime import datetime
from app import db
from app.models.place import Place
from app.models.user import User


class Review(db.Model):
    """SQLAlchemy model for Review"""

    __tablename__ = 'reviews'

    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, text, rating, place, user):
        """Initialize a Review with text, rating, place, and user"""

        if not text:
            raise ValueError("Review text is required")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        if not isinstance(place, Place):
            raise ValueError("place must be a Place instance")
        if not isinstance(user, User):
            raise ValueError("user must be a User instance")

        self.id = str(uuid.uuid4())
        self.text = text
        self.rating = rating
        self.place_id = place.id
        self.user_id = user.id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
