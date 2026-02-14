import uuid
from datetime import datetime

class Amenity:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not name or len(name) > 50:
            raise ValueError("Amenity name is required and must be <= 50 characters")

        self.name = name

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
