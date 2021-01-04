from flask import Blueprint

bp_produtos = Blueprint('produtos', __name__)

@bp_produtos.route('/login',  methods=['GET'])
def login():
    ...
