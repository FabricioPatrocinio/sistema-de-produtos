from flask import Blueprint

bp_financeiro = Blueprint('bp_financeiro', __name__, static_folder='static', template_folder='templates')

from . import views
