#!/usr/bin/python3
""" Documentation """

from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request, Response
from models.amenity import Amenity
from models import storage
import json

@app_views.route('/amenities', strict_slashes=False)
def amenities():
    """
    Return all Amenities
    """
    allAmenities = storage.all('Amenity').values()
    objAmenity = []
    for obj in allAmenities:
        objAmenity.append(obj.to_dict())

    return jsonify(objAmenity)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def list_amenity(amenity_id):
    """
    Return to state for the id
    """
    theAmenity = storage.get('Amenity', amenity_id)
    if theAmenity is None:
        abort(404)

    theAmenity = theAmenity.to_dict()
    return jsonify(theAmenity)

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Create the new amenity object
    """
    if not request.json:
        abort(400, "Not a JSON")
    data = request.json

    if "name" not in data.keys():
        abort(400, "Missing name")

    instance = Amenity(**data)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Update any amenity object
    """
    theAmenity = storage.get('Amenity', amenity_id)
    if theAmenity is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    for key, value in data.items():
        setattr(theAmenity, key, value)
    storage.save()

    return make_response(jsonify(theAmenity.to_dict()), 200)

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """
    Delete object StaAmenityte
    """
    theAmenity = storage.get('Amenity', amenity_id)
    if theAmenity is None:
        abort(404)

    storage.delete(theAmenity)
    storage.save()

    return make_response(jsonify({}), 200)