import uuid
from datetime import datetime
from app.models.user import User
from app.models.amenity import Amenity

class Place:
    def __init__(self, title, description, price, latitude, longitude, owner):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

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

        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner = owner

        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        from app.models.review import Review

        if not isinstance(review, Review):
            raise ValueError("Invalid review")

        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise ValueError("Invalid amenity")

        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
