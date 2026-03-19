#!/usr/bin/python3
"""Flask routes for HBNB Part3 API"""

from flask import Flask, request, jsonify
from app import app, db
from app.models.user import User
from app.models.place import Place

# -------------------------
# Users Endpoints
# -------------------------
@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check for unique email
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(email=email, password=password, first_name=first_name, last_name=last_name)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "email": user.email}), 201


# -------------------------
# Places Endpoints
# -------------------------
@app.route('/places', methods=['POST'])
def create_place():
    """Create a new place"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    title = data.get("title")
    description = data.get("description", "")
    price = data.get("price")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    user_id = data.get("user_id")

    if not all([title, price, latitude, longitude, user_id]):
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        place = Place(
            title=title,
            description=description,
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner=user
        )
        db.session.add(place)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "user_id": place.user_id
    }), 201
