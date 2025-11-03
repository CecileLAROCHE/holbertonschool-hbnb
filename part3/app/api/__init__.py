from flask import Blueprint
from flask_restx import Api
from app.api.v1.users import api as users_ns

bp_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(bp_v1)

# Ajouter ton namespace
api.add_namespace(users_ns, path='/users')
