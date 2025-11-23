from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# -----------------------------
# USERS CRUD
# -----------------------------


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            facade.create_user(user_data)
            new_user = facade.get_user_by_email(user_data["email"])
            return new_user.to_dict(excluded_attr=["password"]), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    @jwt_required()
    def get(self):
        """Retrieve a list of users"""
        users = facade.get_users()
        return [user.to_dict(excluded_attr=[]) for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @jwt_required()
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Not Authenticated')
    @api.response(403, 'Cannot access to this resource')
    @api.response(404, 'User not found')
    def put(self, user_id):
        user_data = api.payload
        sub = get_jwt_identity()
        is_admin = get_jwt().get("is_admin", False)
        if sub != user_id and not is_admin:
            return {'error': 'Cannot access to this resource'}, 403
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        try:
            facade.update_user(user_id, user_data)
            return user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400

# -----------------------------
# USER PLACES
# -----------------------------


@api.route('/<int:user_id>/places')
class UserPlaces(Resource):
    @jwt_required()
    def get(self, user_id):
        """Get all places for a given user"""
        # On récupère l'utilisateur via le facade
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        # Vérification que le user connecté est bien le propriétaire
        if user.id != get_jwt_identity():
            return {"error": "Unauthorized"}, 403

        # Récupération des places via le facade
        places = facade.get_places_by_user(user_id)
        return [place.to_dict() for place in places], 200
