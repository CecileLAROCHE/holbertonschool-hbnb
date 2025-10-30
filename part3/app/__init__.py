from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.api.v1.auth import api as auth_ns

# importe le dictionnaire de config
from config import config

# Import des namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

# instance globale
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_name='default'):
    """Application Factory : crée et configure l'app Flask"""
    app = Flask(__name__)

    # Charger la configuration choisie
    app.config.from_object(config[config_name])

    # Initialiser Bcrypt avec l’app
    bcrypt.init_app(app)
    # Initialiser JWT avec l'app
    jwt.init_app(app)

    # Initialiser l’API RESTX
    api = Api(
        app, version='1.0',
        title='HBnB API',
        description='HBnB Application API')

    # Ajouter les namespaces (endpoints de l’API)
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
