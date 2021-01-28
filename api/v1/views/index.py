#!/usr/bin/python3
"""
Documentation
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status',  strict_slashes=False)
def status():
    """  that returns a JSON: "status": "OK" """
    return jsonify({"status": "OK"})
