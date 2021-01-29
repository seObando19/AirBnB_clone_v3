#!/usr/bin/python3
""" Documentation """

from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models.city import City
from models import storage
import json


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def list_cities(state_id):
    """
    Retrieves the list of all City objects
    """
    theState = storage.get('State', state_id)
    if theState is None:
        abort(404)

    cities = [city.to_dict() for city in theState.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def city(city_id):
    """
    Return to city for the id
    """
    theCity = storage.get('City', city_id)
    if theCity is None:
        abort(404)

    theCity = theCity.to_dict()
    return jsonify(theCity)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Create the new city object
    """
    if not request.json:
        abort(400, "Not a JSON")
    data = request.json

    if "name" not in data.keys():
        abort(400, "Missing name")

    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    data["state_id"] = state_id
    instance = City(**data)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """
    Update any city object
    """
    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    city = storage.get('City', city_id)

    for key, value in data.items():
        setattr(city, key, value)
    storage.save()

    return make_response(jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Delete object City
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)
