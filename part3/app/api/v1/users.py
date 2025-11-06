from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from app.services import facade
from app.api.v1.auth import is_admin


# Création d'un espace de nom (namespace) pour organiser les routes
# liées aux utilisateurs
# Cela permet de regrouper toutes les routes / opérations
# concernant les "users"
api = Namespace('users', description='User operations')

# Définition du modèle de données attendu pour un utilisateur
# Ce modèle sert à la fois pour :
# - la validation automatique des entrées (via @api.expect)
# - la documentation Swagger générée automatiquement par Flask-RESTX
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True,
                              description='Password of the user')
})


# ---------- ROUTE : /users/ ----------
@api.route('/')
class UserList(Resource):
    # Endpoint POST /users/
    # Vérifie que le corps de la requête correspond au modèle user_model
    @api.expect(user_model, validate=True)
    # Réponse possible : création réussie
    @api.response(201, 'User successfully created')
    # Réponse possible : email déjà existant
    @api.response(400, 'Email already registered')
    # Réponse possible : données invalides
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        # Récupère les données envoyées dans le corps de la requête (JSON)
        user_data = api.payload

        # Vérifie si l'email existe déjà via la couche "facade"
        # (simule la vérification dans la base de données)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            # Retourne une erreur si l'email est déjà enregistré
            return {'error': 'Email already registered'}, 400

        try:
            # Crée un nouvel utilisateur via la façade (service métier)
            # Récupération et suppression du mot de passe du dictionnaire
            password = user_data.pop('password')
            # Crée un nouvel utilisateur avec le mot de passe
            new_user = facade.create_user(user_data, password=password)
            # Retourne uniquement les infos publiques (sans mot de passe)
            return new_user.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400


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
        new_user = facade.create_user(user_data, password=password)
        return new_user.to_dict(), 201

    # Endpoint GET /users/
    # Réponse de succès
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
    # Endpoint GET /users/<user_id>
    # Réponse si trouvé
    @api.response(200, 'User details retrieved successfully')
    # Réponse si introuvable
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        # Recherche l'utilisateur par ID via la façade
        user = facade.get_user(user_id)
        if not user:
            # Si aucun utilisateur trouvé, renvoie une erreur 404
            return {'error': 'User not found'}, 404
        # Sinon, renvoie les détails de l'utilisateur
        return user.to_dict(), 200

    # Endpoint PUT /users/<user_id>
    # Attend un corps de requête conforme au modèle user_model
    @api.expect(user_model)
    # Réponse : mise à jour réussie
    @api.response(200, 'User updated successfully')
    # Réponse : mise à jour réussie
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
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
