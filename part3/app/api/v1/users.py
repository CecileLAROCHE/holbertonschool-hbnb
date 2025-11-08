from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from app.services import get_facade
from app.api.v1.auth import is_admin
from app import db
from app.models.user import User

# ✅ Initialise la façade
facade = get_facade()

# Namespace pour organiser les routes utilisateurs
api = Namespace('users', description='User operations')

# Modèle de données attendu pour un utilisateur
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True,
                           description='Email of the user'),
    'password': fields.String(required=True,
                              description='Password of the user')
})


# ---------- UTILITAIRES ----------
def user_exists_response(user, message="Email already registered"):
    """Retourne un dict uniforme lorsque l'utilisateur existe déjà"""
    # Sécuriser si user est un tuple
    if isinstance(user, tuple):
        user = user[0]
    return {
        "error": message,
        "id": str(user.id),
        "is_admin": user.is_admin
    }, 400


# ---------- ROUTE : /users/ ----------
@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        """Register a new user"""
        user_data = api.payload

        if not user_data.get('password'):
            return {'error': 'Password is required'}, 400

        password = user_data.pop('password')
        user, created = facade.create_user(user_data, password=password)

        if not created:
            return user_exists_response(user)

        # Sécuriser si user est tuple
        if isinstance(user, tuple):
            user = user[0]

        return user.to_dict(), 201

    @jwt_required()
    def get(self):
        """Récupère tous les utilisateurs (admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        users = facade.get_users()
        # sécuriser si tuple
        users_list = [u[0] if isinstance(u, tuple) else u for u in users]
        return [u.to_dict() for u in users_list], 200


# ---------- ROUTE : /users/first_admin ----------
@api.route('/first_admin')
class FirstAdmin(Resource):
    def post(self):
        """Créer le premier administrateur s'il n'existe pas déjà"""
        admin_data = {
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "is_admin": True
        }

        admin, created = facade.create_user(admin_data, password="admin")

        if not created:
            return user_exists_response(admin, message="Admin already exists")

        # Sécuriser si admin est tuple
        if isinstance(admin, tuple):
            admin = admin[0]

        return {"message": "First admin created", "id": str(admin.id)}, 201


# ---------- ROUTE : /users/admin/ ----------
@api.route('/admin')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        """Create a new admin (admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        password = user_data.pop('password', None)
        if not password:
            return {'error': 'Password is required'}, 400

        user, created = facade.create_user(user_data, password=password)

        if not created:
            return user_exists_response(user)

        # Sécuriser si user est tuple
        if isinstance(user, tuple):
            user = user[0]

        return user.to_dict(), 201

    @jwt_required()
    def get(self):
        """Récupère tous les admins (admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        users = facade.get_users()
        # sécuriser si tuple
        users_list = [u[0] if isinstance(u, tuple) else u for u in users]

        # filtrer uniquement les admins
        admins_list = [u for u in users_list if u.is_admin]

        return [u.to_dict() for u in admins_list], 200


# ---------- ROUTE : /users/<user_id> ----------
@api.route('/<user_id>')
class UserResource(Resource):
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if isinstance(user, tuple):
            user = user[0]

        return user.to_dict(), 200

    @api.expect(user_model)
    def put(self, user_id):
        """Update a user by ID"""
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if isinstance(user, tuple):
            user = user[0]

        try:
            facade.update_user(user_id, user_data)
            return user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400


# ---------- ROUTE : /users/setup-admin/ ----------
@api.route('/setup-admin')
class SetupAdmin(Resource):
    def post(self):
        """Créer un admin par défaut si inexistant"""
        admin_data = {
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "password": "StrongSecurePassword",
            "is_admin": True
        }

        admin, created = facade.create_user(admin_data,
                                            password=admin_data["password"])

        if not created:
            return user_exists_response(admin, message="Admin already exists")

        if isinstance(admin, tuple):
            admin = admin[0]

        return {"id": str(admin.id), "message": "Admin created"}, 201


# ---------- ROUTE : /users/admins/ ----------
@api.route('/admins')
class AdminList(Resource):
    @jwt_required()
    def get(self):
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        admins = facade.get_all_admins()
        if not admins:
            return {'message': 'No admin users found'}, 200

        return [a.to_dict() for a in admins], 200


# ---------- ROUTE : /users/clear_all ----------
@api.route('/clear_all')
class ClearAllUsers(Resource):
    def delete(self):
        """⚠️ Supprime tous les utilisateurs de la base
        (uniquement pour les tests)."""
        users = User.query.all()
        if not users:
            return {"message": "Aucun utilisateur à supprimer"}, 200

        count = len(users)
        for user in users:
            db.session.delete(user)
        db.session.commit()

        print(
            f"🗑️ Tous les utilisateurs ({count}) "
            f"ont été supprimés de la base."
        )
        return {"message": f"{count} utilisateurs supprimés"}, 200
