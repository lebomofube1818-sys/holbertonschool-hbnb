from flask import request
from flask_restx import Namespace, Resource, fields
from app.models.place import Place
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('places', description='Place related operations')

# API model for serialization
place_model = api.model('Place', {
    'id': fields.String(readonly=True),
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price of the place'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(description='ID of the owner user')
})

# Temporary in-memory storage for Place objects
places_list = []

# Helper function to find user by id
def get_user_by_id(user_id):
    return User.all_users.get(user_id)

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
        """Get all places"""
        return places_list

    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new place"""

        current_user_id = get_jwt_identity()
        data = api.payload
        print(User.all_users)
        print(current_user_id)
        owner = get_user_by_id(current_user_id)

        if not owner:
            api.abort(404, "Authenticated user not found")

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
        return place

    @api.expect(place_model)
    @api.marshal_with(place_model)
    @jwt_required()
    def put(self, place_id):
        """Update a specific place by ID"""

        current_user_id = get_jwt_identity()

        place = get_place_by_id(place_id)

        if not place:
            api.abort(404, f"Place with id {place_id} not found")

        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        if not is_admin and place.owner.id != current_user_id:
            api.abort(403, "Unauthorized action")
        data = api.payload

        # Prevent owner change
        if 'owner_id' in data:
            del data['owner_id']

        place.update(data)

        return place
