from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.extensions import bcrypt, jwt, db
from app.database import init_db, seed_db
from flask_cors import CORS


def create_app(config_class="config.DevelopmentConfig"):
    # Flask app avec dossier static
    app = Flask(__name__, static_folder="static", static_url_path="")

    # ⚡ CORS pour dev local avec support des cookies
    CORS(
        app,
        resources={r"/api/*": {
            "origins": [
                "http://127.0.0.1:5000",
                "http://localhost:5000"
            ]
        }},
        supports_credentials=True
    )

    # Configuration
    app.config.from_object(config_class)

    # API Flask-RESTX
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API'
    )

    # Extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Initialisation base de données
    with app.app_context():
        init_db()
        seed_db()

    # Enregistrement des namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
