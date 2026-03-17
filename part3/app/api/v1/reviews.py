from datetime import datetime
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.review import Review
from app.models.place import Place
from app.models.user import User

api = Namespace('reviews', description='Review related operations')

# API model
review_model = api.model('Review', {
    'id': fields.String(readonly=True),
    'text': fields.String(required=True, description='Review text'),
    'user_id': fields.String(readonly=True, description='User who wrote the review'),
    'place_id': fields.String(required=True, description='Place being reviewed')
})

# Temporary storage
reviews_list = []


# -----------------------
# Helper functions
# -----------------------

def get_user_by_id(user_id):
    return User.all_users.get(user_id)  # returns User object or None


def get_place_by_id(place_id):
    return Place.all_places.get(place_id)


def get_review_by_id(review_id):
    for review in reviews_list:
        if review.id == review_id:
            return review
    return None


# -----------------------
# Create Review
# -----------------------

@api.route('/')
class ReviewList(Resource):

    @api.expect(review_model)
    @api.marshal_with(review_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new review"""

        data = api.payload
        current_user_id = get_jwt_identity()

        user = get_user_by_id(current_user_id)
        place = get_place_by_id(data['place_id'])

        if not place:
            api.abort(404, "Place not found")

        new_review = Review(
            text=data['text'],
            user=user,
            place=place
        )

        reviews_list.append(new_review)

        # Attach review to place
        if not hasattr(place, "reviews"):
            place.reviews = []

        place.reviews.append(new_review)

        return new_review, 201


# -----------------------
# Get Reviews for Place
# -----------------------

@api.route('/places/<string:place_id>')
class PlaceReviews(Resource):

    @api.marshal_list_with(review_model)
    def get(self, place_id):
        """Get all reviews for a place"""

        place = get_place_by_id(place_id)

        if not place:
            api.abort(404, "Place not found")

        return getattr(place, "reviews", [])


# -----------------------
# Review Detail
# -----------------------

@api.route('/<string:review_id>')
class ReviewDetail(Resource):

    @api.marshal_with(review_model)
    def get(self, review_id):
        """Get a review by ID"""

        review = get_review_by_id(review_id)

        if not review:
            api.abort(404, "Review not found")

        return review

    @api.expect(review_model)
    @api.marshal_with(review_model)
    @jwt_required()
    def put(self, review_id):
        """Update a review dynamically"""

        current_user_id = get_jwt_identity()

        review = get_review_by_id(review_id)

        if not review:
            api.abort(404, "Review not found")

        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        if not is_admin and review.user.id != current_user_id:
            api.abort(403, "Unauthorized action")

        data = api.payload

        # Fields that cannot be updated
        protected_fields = {'id', 'user_id', 'place_id'}

        # Update allowed fields dynamically
        for key, value in data.items():
            if key not in protected_fields and hasattr(review, key):
                setattr(review, key, value)

        # Update timestamp
        if hasattr(review, "updated_at"):
            review.updated_at = datetime.now()

        return review

    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""

        current_user_id = get_jwt_identity()

        review = get_review_by_id(review_id)

        if not review:
            api.abort(404, "Review not found")

        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        if not is_admin and review.user.id != current_user_id:
            api.abort(403, "Unauthorized action")

        reviews_list.remove(review)

        return {"message": "Review deleted"}, 200
