#!/usr/bin/python3
""" Documentation """

from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request, Response
from models.user import User
from models import storage
import json


@app_views.route('/users', strict_slashes=False)
def users():
    """
    Return all users
    """
    allUser = storage.all('User').values()
    objUser = []
    for obj in allUser:
        objUser.append(obj.to_dict())

    return jsonify(objUser)


@app_views.route('/users/<user_id>', strict_slashes=False)
def list_user(user_id):
    """
    Return to user for the id
    """
    theUser = storage.get('State', user_id)
    if theUser is None:
        abort(404)

    theUser = theUser.to_dict()
    return jsonify(theUser)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Create the new user object
    """
    if not request.json:
        abort(400, "Not a JSON")
    data = request.json

    if "name" not in data.keys():
        abort(400, "Missing name")

    instance = User(**data)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Update any user object
    """
    theUser = storage.get('User', user_id)
    if theUser is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    for key, value in data.items():
        setattr(theUser, key, value)
    storage.save()

    return make_response(jsonify(theUser.to_dict()), 200)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def user_delete(user_id):
    """
    Delete object User
    """
    theUser = storage.get('User', user_id)
    if theUser is None:
        abort(404)

    storage.delete(theUser)
    storage.save()

    return make_response(jsonify({}), 200)
