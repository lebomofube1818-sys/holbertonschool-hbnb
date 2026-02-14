import uuid
from datetime import datetime
from app.models.place import Place
from app.models.user import User

class Review:
    def __init__(self, text, rating, place, user):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not text:
            raise ValueError("Review text is required")

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        if not isinstance(place, Place):
            raise ValueError("Place must be a Place instance")

        if not isinstance(user, User):
            raise ValueError("User must be a User instance")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
