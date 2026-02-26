import uuid
import re
from datetime import datetime

class User:
    def __init__(self, first_name, last_name, email, is_admin=False):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not first_name or len(first_name) > 50:
            raise ValueError("first_name is required and must be <= 50 characters")

        if not last_name or len(last_name) > 50:
            raise ValueError("last_name is required and must be <= 50 characters")

        if not email or not self._is_valid_email(email):
            raise ValueError("Invalid email format")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = bool(is_admin)

    def _is_valid_email(self, email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    # <-- ADD THIS METHOD
    def to_dict(self):
        """Return a dictionary representation of the user including the id."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class Review:
    def __init__(self, text, user_id, place_id, storage):
        if not text or not text.strip():
            raise ValueError("text cannot be empty")

        if not storage.get_user(user_id):
            raise ValueError("Invalid user_id")

        if not storage.get_place(place_id):
            raise ValueError("Invalid place_id")

        self.id = str(uuid.uuid4())
        self.text = text
        self.user_id = user_id
        self.place_id = place_id
