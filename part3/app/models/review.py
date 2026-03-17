#!/usr/bin/python3
"""Review Model"""

import uuid
from datetime import datetime
from app import db


class Review(db.Model):
    """SQLAlchemy model for Review"""

    __tablename__ = 'reviews'

    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(60), nullable=False)  # store the place's id
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, text, rating, place_id):
        if not text:
            raise ValueError("Review text is required")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        if not place_id:
            raise ValueError("place_id is required")

        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
