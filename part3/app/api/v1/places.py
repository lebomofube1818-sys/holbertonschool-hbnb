#!/usr/bin/python3
"""Places API endpoints"""

import uuid
from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.place import Place
from app.models.user import User

api = Namespace('places', description='Place related operations')

# API model for serialization
place_model = api.model('Place', {
    'id': fields.String(readonly=True),
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price of the place'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(description='ID of the owner user')
})

# Helper functions
def get_place_by_id(place_id):
    return Place.query.get(place_id)

def get_user_by_id(user_id):
    return User.query.get(user_id)

# Routes
@api.route('/')
class PlaceList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        """Get all places"""
        return Place.query.all()

    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    @jwt_required()
    def post(self):
        """Create a new place"""
        current_user_id = get_jwt_identity()
        data = api.payload
        owner = get_user_by_id(current_user_id)

        if not owner:
            api.abort(404, "Authenticated user not found")

        new_place = Place(
            title=data['title'],
            description=data.get('description', ''),
            price=float(data['price']),
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            owner=owner
        )

        db.session.add(new_place)
        db.session.commit()

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

        if place.owner_id != current_user_id:
            api.abort(403, "Unauthorized action")

        data = api.payload
        # Prevent owner change
        data.pop('owner_id', None)

        for key, value in data.items():
            setattr(place, key, value)
        place.updated_at = datetime.utcnow()

        db.session.commit()

        return place
