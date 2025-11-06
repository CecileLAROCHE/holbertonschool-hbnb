from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from app.services import get_facade
from app.api.v1.auth import is_admin
from app import db

# ✅ Initialise la façade ici
facade = get_facade()

# Création d'un espace de nom (namespace) pour organiser les routes liées aux utilisateurs
api = Namespace('users', description='User operations')

# Définition du modèle de données attendu pour un utilisateur
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


# ---------- ROUTE : /users/ ----------
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

        if not user_data.get('password'):
            return {'error': 'Password is required'}, 400

        try:
            password = user_data.pop('password')
            new_user = facade.create_user(user_data, password=password)
            return new_user.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/first_admin')
class FirstAdmin(Resource):
    def post(self):
        # Vérifie si un utilisateur avec cet email existe déjà
        from app.models.user import User
        existing_user = User.query.filter_by(email="admin@example.com").first()
        if existing_user:
            return {"error": "Admin already exists"}, 400

        # Données du premier admin
        admin_data = {
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "is_admin": True
        }

        # Crée l'admin avec mot de passe par défaut
        admin = facade.create_user(admin_data, password="admin")
        return {"message": "First admin created", "id": str(admin.id)}, 201


@api.route('/admin/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        """Créer un nouvel utilisateur (Admin uniquement)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        if facade.get_user_by_email(user_data.get('email')):
            return {'error': 'Email already registered'}, 400

        password = user_data.pop('password', None)
        if not password:
            return {'error': 'Password is required'}, 400
        new_user = facade.create_user(user_data, password=password)
        return new_user.to_dict(), 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of users (admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403
        users = facade.get_users()
        return [user.to_dict() for user in users], 200


# ---------- ROUTE : /users/<user_id> ----------
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

    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update a user by ID"""
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        try:
            facade.update_user(user_id, user_data)
            return user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/setup-admin/')
class SetupAdmin(Resource):
    def post(self):
        admin_data = {
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "password": "StrongSecurePassword",
            "is_admin": True
        }

        if not facade.get_user_by_email(admin_data["email"]):
            admin = facade.create_user(admin_data,
                                       password=admin_data["password"])
            return {"id": str(admin.id), "message": "Admin created"}, 201
        else:
            return {"message": "Admin already exists"}, 200


@api.route('/admins/')
class AdminList(Resource):
    @jwt_required()
    def get(self):
        """Retrieve all admin users (admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        admins = facade.get_all_admins()

        if not admins:
            return {'message': 'No admin users found'}, 200

        return [admin.to_dict() for admin in admins], 200
