from flask import Flask, Blueprint
from flask_restx import Api
from app.api.v1.users import api as users_ns

def create_app(config_name):
    app = Flask(__name__)
    
    # Configs et db.init_app(app) si besoin
    from app.models.basemodel import db
    db.init_app(app)

    # Créer un blueprint pour l'API v1
    bp_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
    api = Api(bp_v1)

    # Ajouter le namespace "users"
    api.add_namespace(users_ns, path='/users')

    # Enregistrer le blueprint
    app.register_blueprint(bp_v1)

    return app
