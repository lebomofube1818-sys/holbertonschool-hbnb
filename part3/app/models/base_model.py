#!/usr/bin/python3
"""Base model for all other models"""

import uuid
from datetime import datetime


class BaseModel:
    """Defines common attributes and methods for all models"""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Updates the updated_at timestamp"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Returns dictionary representation of the instance"""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

