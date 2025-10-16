from flask_restx import Namespace, Resource, fields
from app.services import facade
import re


api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
    })


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Invalid email format')
    def post(self):
        """Register a new user"""

        user_data = api.payload

        if (
            not user_data.get('first_name')
            or not user_data.get('last_name')
            or not user_data.get('email')
            ):
            return {"error": "Invalid input data"}, 400

        if not re.match(r"[^@]+@[^@]+\.[^@]+", user_data['email']):
            return {"error": "Invalid email format"}, 400

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {"error": "Email already registered"}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201

        except Exception:
            return {"error": "Invalid input data"}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve list of all users"""
        users = facade.get_all_users()
        user_list = [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            }
            for u in users
        ]
        return user_list, 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update an existing user"""
        user_data = api.payload or {}

        # Vérifie que le user existe
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Validation du format de l'email si fourni
        if 'email' in user_data:
            email = user_data['email']
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return {"error": "Invalid email format"}, 400

        # Met à jour seulement les champs fournis
        updatable_fields = ['first_name', 'last_name', 'email']
        for key, value in user_data.items():
            if key in updatable_fields and value is not None:
                setattr(user, key, value)

        # Sauvegarde la mise à jour via la façade
        updated_user = facade.update_user(user_id, user_data)

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200
