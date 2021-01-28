#!/usr/bin/python3
"""
Documentation
"""


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.users import *


