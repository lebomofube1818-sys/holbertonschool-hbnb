from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Review model for API validation and serialization
review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='Review ID'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model, code=201)
    def post(self):
        """Register a new review"""
        data = api.payload
        try:
            review = facade.create_review(data)
        except ValueError as e:
            return {"error": str(e)}, 400
        return review.__dict__, 201

    @api.marshal_list_with(review_model)
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [r.__dict__ for r in reviews], 200

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, f"Review with id {review_id} not found")
        return review.__dict__

    @api.expect(review_model, validate=True)
    @api.marshal_with(review_model)
    def put(self, review_id):
        """Update a review's information"""
        data = api.payload
        try:
            review = facade.update_review(review_id, data)
        except ValueError as e:
            return {"error": str(e)}, 400
        if not review:
            api.abort(404, f"Review with id {review_id} not found")
        return review.__dict__

    def delete(self, review_id):
        """Delete a review"""
        review = facade.delete_review(review_id)
        if not review:
            api.abort(404, f"Review with id {review_id} not found")
        return {"message": "Review deleted successfully"}, 200
