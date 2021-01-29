from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(200), nullable=False)
    img_perfil = db.Column(db.String(255), nullable=True)
    produtos = db.relationship('Produtos', backref='users')
    referencia = db.relationship('Referencia', backref='users')
    fabricante = db.relationship('Fabricante', backref='users')
    tipo = db.relationship('Tipo', backref='users')
    
    def __init__(self, nome, email, senha,img_perfil):
        self.nome = nome
        self.email = email
        self.senha = generate_password_hash(senha)
        self.img_perfil = img_perfil
    
    def verify_password(self, pwd):
        return check_password_hash(self.senha, pwd)

class Produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cod = db.Column(db.Integer, nullable=True, unique=True)
    descricao = db.Column(db.String(50), nullable=False)
    complemento = db.Column(db.String(255))
    referencia = db.Column(db.Integer, db.ForeignKey('referencia.id'))
    fabricante = db.Column(db.Integer, db.ForeignKey('fabricante.id'))
    tipo = db.Column(db.Integer, db.ForeignKey('tipo.id'))
    quant = db.Column(db.Integer, default=0)
    custo = db.Column(db.Integer, default=0)
    preco = db.Column(db.Integer, default=0)
    
    def __init__(self, user_id, cod, descricao, complemento, referencia, fabricante, tipo, quant, custo, preco):
        self.user_id = user_id
        self.cod = cod
        self.descricao = descricao
        self.complemento = complemento
        self.referencia = referencia
        self.fabricante = fabricante
        self.tipo = tipo
        self.quant = quant
        self.custo = custo
        self.preco = preco

class Referencia(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    produtos = db.relationship('Produtos', backref='referencia_id')
    
    def __init__(self, nome, user_id):
        self.nome = nome
        self.user_id = user_id

class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    produtos = db.relationship('Produtos', backref='fabricante_id')
    
    def __init__(self, nome, user_id):
        self.nome = nome
        self.user_id = user_id

class Tipo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    produtos = db.relationship('Produtos', backref='tipo_id')
    
    def __init__(self, nome, user_id):
        self.nome = nome
        self.user_id = user_id
