#!/usr/bin/python3
"""
Module Docs
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """
    Function Docs
    """
    try:
        city_list = []
        state_list = storage.all('City')
        for key, value in state_list.items():
            city_dict = value.to_dict()
            if city_dict.get('state_id') == state_id:
                city_list.append(city_dict)
        return jsonify(city_list)
    except BaseException:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """
    Function Docs
    """
    try:
        city = storage.get('City', city_id)
        return jsonify(city.to_dict())
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Function Docs
    """
    try:
        city = storage.get('City', city_id)
        storage.delete(city)
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """
    Function Docs
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    city = City(**request.get_json())
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """
    Function Docs
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'state_id', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
