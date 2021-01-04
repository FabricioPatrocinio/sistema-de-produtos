from flask_marshmallow import Marshmallow
from .model import Produtos

ma = Marshmallow()

def configure(app):
    ma.init_app(app)


class ProdutosSchema(ma.Schema):
    class Meta:
        model = Produtos
