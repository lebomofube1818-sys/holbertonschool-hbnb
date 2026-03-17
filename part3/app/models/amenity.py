#!/usr/bin/python3
"""Amenity model"""

import uuid
from datetime import datetime
from app import db

class Amenity(db.Model):
    """SQLAlchemy model for Amenity"""

    __tablename__ = 'amenities'

    id = db.Column(db.String(60), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not name or len(name) > 50:
            raise ValueError("Amenity name is required")

        self.name = name

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
