from flask import Blueprint

bp_produtos = Blueprint('produtos', __name__, template_folder='templates', static_folder='static')

from .produtos import produtos
