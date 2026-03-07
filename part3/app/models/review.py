import uuid
from datetime import datetime
from app.models.place import Place
from app.models.user import User


class Review:
    def __init__(self, text, place, user, rating=None):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not text:
            raise ValueError("Review text is required")
        self.text = text

        # Rating is optional, but if provided must be 1-5
        if rating is not None:
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                raise ValueError("Rating must be an integer between 1 and 5")
        self.rating = rating

        if not isinstance(place, Place):
            raise ValueError("Place must be a Place instance")
        self.place = place
        self.place_id = place.id

        if not isinstance(user, User):
            raise ValueError("User must be a User instance")
        self.user = user
        self.user_id = user.id
