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
    
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = generate_password_hash(senha)
    
    def verify_password(self, pwd):
        return check_password_hash(self.senha, pwd)

class Produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod = db.Column(db.Integer, nullable=True, unique=True)
    descricao = db.Column(db.String(50), nullable=False)
    complemento = db.Column(db.String(255))
    referencia = db.Column(db.String(50))
    fabricante = db.Column(db.String(50))
    tipo = db.Column(db.String(50))
    quant = db.Column(db.Integer, default=0)
    custo = db.Column(db.Integer, default=0)
    preco = db.Column(db.Integer, default=0)
    
    def __init__(self, cod, descricao, complemento, referencia, fabricante, tipo, quant, custo, preco):
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
    
    def __init__(self, nome):
        self.nome = nome

class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    
    def __init__(self, nome):
        self.nome = nome

class Tipo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(30), nullable=False)
    
    def __init__(self, nome):
        self.nome = nome
