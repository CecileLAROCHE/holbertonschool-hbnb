from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import get_facade
from flask import request


# ✅ initialise correctement la façade
facade = get_facade()

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})



@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload

        # 1️⃣ Retrieve user from DB
        user = facade.get_user_by_email(credentials['email'])

        # 2️⃣ Check credentials
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # 3️⃣ Create JWT
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )

        # 4️⃣ Return token
        return {'access_token': access_token}, 200


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        return {'message': f'Hello, user {user_id}'}, 200


def is_admin():
    """Vérifie si l'utilisateur courant est un administrateur."""
    claims = get_jwt()
    return claims.get('is_admin', False)


def current_user_id():
    """Retourne l'ID de l'utilisateur courant à partir du JWT."""
    return get_jwt_identity()
