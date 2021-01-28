#!/usr/bin/python3
"""
Documentation
"""
from os import getenv
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_api(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def pega_not_found(e):
    """
    create a handler for 404 errors that returns a
    JSON-formatted 404 status
    """
    res = {"error": "Not found"}
    return make_response(jsonify(res), 404)

if __name__ == '__main__':
    app.run(host=(getenv('HBNB_API_HOST', '0.0.0.0')),
            port=(getenv('HBNB_API_PORT', '5000')),
            threaded=True,
            debug=True)
