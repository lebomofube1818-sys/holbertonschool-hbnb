#!/usr/bin/python3
"""Base model for all other models"""

from app import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    """Defines common attributes and methods for all models"""
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))

    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow)

    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def to_dict(self):
        """Returns dictionary representation of the instance"""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
