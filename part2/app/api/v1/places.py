from flask_restx import Namespace, Resource, fields
from app.models.place import Place
from app.services.facade import facade

api = Namespace('places', description='Place related operations')

# API model for reviews inside a place
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# API model for serialization
place_model = api.model('Place', {
    'id': fields.String(readonly=True),
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price of the place'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='ID of the owner user'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews for this place')
})

# Temporary in-memory storage for Place objects
places_list = []

# Helper function to find place by id
def get_place_by_id(place_id):
    for place in places_list:
        if place.id == place_id:
            return place
    return None

@api.route('/')
class PlaceList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        """Get all places including their reviews"""
        result = []
        for place in places_list:
            place_data = place.__dict__.copy()
            # Include reviews as a list of dicts
            place_data['reviews'] = [r.__dict__ for r in getattr(place, 'reviews', [])]
            result.append(place_data)
        return result

    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        data = api.payload

        # Use facade to get the user by ID
        owner = facade.get_user(data['owner_id'])
        if not owner:
            api.abort(400, f"User with id {data['owner_id']} does not exist")

        new_place = Place(
            title=data['title'],
            description=data.get('description', ''),
            price=data['price'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            owner=owner
        )

        places_list.append(new_place)
        return new_place, 201

@api.route('/<string:place_id>')
class PlaceDetail(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Get a specific place by ID"""
        place = get_place_by_id(place_id)
        if not place:
            api.abort(404, f"Place with id {place_id} not found")

        place_data = place.__dict__.copy()
        place_data['reviews'] = [r.__dict__ for r in getattr(place, 'reviews', [])]
        return place_data

    @api.expect(place_model)
    @api.marshal_with(place_model)
    def put(self, place_id):
        """Update a specific place by ID"""
        place = get_place_by_id(place_id)
        if not place:
            api.abort(404, f"Place with id {place_id} not found")

        data = api.payload
        if 'owner_id' in data:
            owner = facade.get_user(data['owner_id'])
            if not owner:
                api.abort(400, f"User with id {data['owner_id']} does not exist")
            data['owner'] = owner
            del data['owner_id']

        place.update(data)
        return place

@api.route('/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.marshal_list_with(fields.Raw)
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = get_place_by_id(place_id)
        if not place:
            api.abort(404, f"Place with id {place_id} not found")

        reviews = facade.get_reviews_by_place(place_id)
        return [r.__dict__ for r in reviews], 200

