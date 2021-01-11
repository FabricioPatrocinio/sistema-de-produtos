from flask import Blueprint

bp_produtos = Blueprint('bp_produtos', __name__, static_folder='static', template_folder='templates')

from . import views
