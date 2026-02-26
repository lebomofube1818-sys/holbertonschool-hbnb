from flask import Flask, request
from flask_restx import Api, Resource, fields
from app.services.place_service import PlaceService

app = Flask(__name__)
api = Api(app)

place_service = PlaceService()

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'owner_id': fields.String(description='Owner ID'),
    'amenities': fields.List(fields.String, description='List of amenities')
})

@api.route('/places')
class PlaceList(Resource):
    @api.expect(place_model)
    def post(self):
        data = request.json
        place = place_service.create_place(data)
        return place.__dict__, 201

    def get(self):
        places = place_service.list_places()
        return [p.__dict__ for p in places]

@api.route('/places/<string:place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        place = place_service.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.__dict__

    @api.expect(place_model)
    def put(self, place_id):
        data = request.json
        place = place_service.update_place(place_id, data)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.__dict__

