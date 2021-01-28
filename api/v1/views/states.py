#!/usr/bin/python3
""" Documentation """

from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request, Response
from models.state import State
from models import storage
import json


@app_views.route('/states', strict_slashes=False)
def states():
    """
    Return all States
    """
    allState = storage.all('State').values()
    objState = []
    for obj in allState:
        objState.append(obj.to_dict())

    return jsonify(objState)


@app_views.route('/states/<state_id>', strict_slashes=False)
def list_state(state_id):
    """
    Return to state for the id
    """
    theState = storage.get('State', state_id)
    if theState is None:
        abort(404)

    theState = theState.to_dict()
    return jsonify(theState)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Create the new state object
    """
    if not request.json:
        abort(400, "Not a JSON")
    data = request.json

    if "name" not in data.keys():
        abort(400, "Missing name")

    instance = State(**data)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Update any state object
    """
    theState = storage.get('State', state_id)
    if theState is None:
        abort(404)

    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    for key, value in data.items():
        setattr(theState, key, value)
    storage.save()

    return make_response(jsonify(theState.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_delete(state_id):
    """
    Delete object State
    """
    theState = storage.get('State', state_id)
    if theState is None:
        abort(404)

    storage.delete(theState)
    storage.save()

    return make_response(jsonify({}), 200)
