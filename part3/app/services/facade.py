from app.services.repositories.user_repository import UserRepository
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(None)
        self.review_repo = SQLAlchemyRepository(None)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None

        # Update only the fields provided
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        # Save changes back to repository
        self.user_repo.update(user)  # <-- only pass the user object

        return user

    # Placeholder methods for later tasks
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)
