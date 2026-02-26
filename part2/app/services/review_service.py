from app.models.review import Review

class ReviewService:
    def __init__(self):
        self.reviews = []  # In-memory storage

    def create_review(self, text, rating, user, place):
        review = Review(text, rating, place, user)
        self.reviews.append(review)
        # Link review to place
        place.reviews.append(review)
        return review

    def get_all_reviews(self):
        return self.reviews

    def get_review(self, review_id):
        for r in self.reviews:
            if r.id == review_id:
                return r
        return None

    def update_review(self, review_id, data):
        review = self.get_review(review_id)
        if review:
            review.update(data)
            return review
        return None

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if review:
            review.place.reviews.remove(review)  # Remove from place
            self.reviews.remove(review)
            return True
        return False

