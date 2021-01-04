from flask import Flask
from flask_migrate import Migrate
from .model import configure as config_db
from .serealizer import configure as config_ma

def create_app():
    app = Flask(__name__)
    
    app.secret_key = 'fsdapiwquuuyqwi@uyasjah-986667655'
    
    app.config["CACHE_TYPE"] = "null"
    app.config['SECRET_KEY'] = 'fsdapiwquuuyqwi@uyasjah-986667655'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost:3306/sistema_produtos'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    config_db(app)
    config_ma(app)
    
    Migrate(app, app.db)
    
    from .produtos import bp_produtos
    app.register_blueprint(bp_produtos)
    
    return app
