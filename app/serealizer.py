from flask_marshmallow import Marshmallow
from .model import Produtos, Users, Referencia, Fabricante, Tipo

ma = Marshmallow()

def configure(app):
    ma.init_app(app)

# Serve para retornar os objetos em json
class ProdutosSchema(ma.Schema):
    class Meta:
        model = Produtos

class UsersSchema(ma.Schema):
    class Meta:
        model = Users

class ReferenciaSchema(ma.Schema):
    class Meta:
        model = Referencia

class FabricanteSchema(ma.Schema):
    class Meta:
        model = Fabricante

class TipoSchema(ma.Schema):
    class Meta:
        model = Tipo