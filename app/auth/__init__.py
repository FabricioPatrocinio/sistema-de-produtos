from flask import Blueprint

bp_auth = Blueprint('bp_auth', __name__, static_folder='static', template_folder='templates')

from . import views
