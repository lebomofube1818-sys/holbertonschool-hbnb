from flask_restx import Namespace, Resource, fields
from app.models.place import Place

ns = Namespace('places', description='Place related operations')

place_model = ns.model('Place', {
    'id': fields.String(readonly=True),
    'title': fields.String(required=True, description='The place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True)
})

@ns.route('/')
class PlaceList(Resource):
    def get(self):
        # Return all places
        return {'message': 'List of places'}

    def post(self):
        # Create a new place
        return {'message': 'Create place'}

