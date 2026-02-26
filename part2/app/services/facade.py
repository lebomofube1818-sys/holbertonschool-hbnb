from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.place import Place


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ---------------- User Methods ----------------
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update an existing user"""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # Prevent duplicate email
        if 'email' in user_data:
            existing_user = self.user_repo.get_by_attribute('email', user_data['email'])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")

        # Update fields
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']

        if 'last_name' in user_data:
            user.last_name = user_data['last_name']

        if 'email' in user_data:
            user.email = user_data['email']

        return user

    # ---------------- Amenity Methods ----------------
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

    # ---------------- Review Methods ----------------
    def create_review(self, review_data):
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])

        if not user:
            raise ValueError(f"User with id {review_data['user_id']} does not exist")
        if not place:
            raise ValueError(f"Place with id {review_data['place_id']} does not exist")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )

        self.review_repo.add(review)

        if not hasattr(place, "reviews"):
            place.reviews = []
        place.reviews.append(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return getattr(place, "reviews", [])

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if 'text' in review_data:
            review.text = review_data['text']

        if 'rating' in review_data:
            if review_data['rating'] not in [1, 2, 3, 4, 5]:
                raise ValueError("Rating must be 1-5")
            review.rating = review_data['rating']

        review.save()
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        self.review_repo.remove(review)

        if hasattr(review.place, "reviews") and review in review.place.reviews:
            review.place.reviews.remove(review)

        return review


# Create a single instance of HBnBFacade to use across your app
facade = HBnBFacade()
