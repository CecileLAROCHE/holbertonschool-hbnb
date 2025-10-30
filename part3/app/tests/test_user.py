import unittest
from app import create_app
from app.models.user import User
from app.persistence.repository import InMemoryRepository
from app import create_app, bcrypt
from app.services.facade import HBnBFacade
from flask_jwt_extended import decode_token


class TestUserModel(unittest.TestCase):
    """Tests unitaires pour la classe User"""

    def setUp(self):
        # Réinitialiser les emails avant chaque test
        User.emails = set()

    def tearDown(self):
        # Nettoyer les emails après chaque test
        User.emails.clear()

    def test_user_creation(self):
        user = User(first_name="John",
                    last_name="Doe",
                    email="john.doe@example.com",
                    password="password")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertFalse(user.is_admin)  # valeur par défaut

        user_id = user.id
        self.assertEqual(user.to_dict(), {
            'id': user_id,
            'first_name': "John",
            'last_name': "Doe",
            'email': "john.doe@example.com"
        })

    def test_user_max_length(self):
        with self.assertRaises(ValueError) as context:
            User(first_name="a" * 60,
                 last_name="Doe",
                 email="john.doe@example.com")
        self.assertEqual(str(context.exception),
                         "First name must be 50 characters max.")

        with self.assertRaises(ValueError) as context:
            User(first_name="John",
                 last_name="b" * 60,
                 email="john.doe@example.com")
        self.assertEqual(str(context.exception),
                         "Last name must be 50 characters max.")

    def test_user_email(self):
        with self.assertRaises(ValueError) as context:
            User(first_name="John",
                 last_name="Doe",
                 email="john.doeexample.com")
        self.assertEqual(str(context.exception), "Invalid email format")

    def test_user_required_fields(self):
        with self.assertRaises(TypeError):
            User(first_name="John", last_name="Doe")

        with self.assertRaises(TypeError):
            User(first_name="John", email="john.doe@example.com")

        with self.assertRaises(TypeError):
            User(last_name="Doe", email="john.doe@example.com")

    def test_user_update(self):
        user = User(first_name="John",
                    last_name="Doe",
                    email="john.doe@example.com")
        new_data = {'first_name': "Jane",
                    'last_name': "Dupont",
                    'email': "jane.dupont@example.com"}
        user.update(new_data)
        self.assertEqual(user.to_dict(), {
            'id': user.id,
            'first_name': "Jane",
            'last_name': "Dupont",
            'email': "jane.dupont@example.com"
        })

    def test_user_update_fail(self):
        user = User(first_name="John",
                    last_name="Doe",
                    email="john.doe@example.com")
        with self.assertRaises(ValueError) as context:
            user.first_name = "a" * 60
        self.assertEqual(str(context.exception),
                         "First name must be 50 characters max.")

        with self.assertRaises(ValueError) as context:
            user.last_name = "b" * 60
        self.assertEqual(str(context.exception),
                         "Last name must be 50 characters max.")

        with self.assertRaises(ValueError) as context:
            user.email = "john.doeexample.com"
        self.assertEqual(str(context.exception), "Invalid email format")


class TestUserEndpoints(unittest.TestCase):
    """Tests d’intégration des endpoints /api/v1/users/"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_create_valid_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_user_bad_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data, {"error": "Invalid email format"})

    def test_get_user_by_id(self):
        create_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Wonder",
            "email": "alice@example.com",
            "password": "password123"
        })
        self.assertEqual(create_resp.status_code, 201)
        user_id = create_resp.get_json()["id"]

        get_resp = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(get_resp.status_code, 200)
        data = get_resp.get_json()
        self.assertEqual(data["email"], "alice@example.com")

    def test_get_nonexistent_user(self):
        repo = InMemoryRepository()
        result = repo.get("non-existent-user-id")
        self.assertIsNone(result)

    def test_update_user(self):
        create_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Marley",
            "email": "bob@example.com",
            "password": "password123"
        })
        self.assertEqual(create_resp.status_code, 201)
        user_id = create_resp.get_json()["id"]

        update_resp = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Robert",
            "last_name": "Marley",
            "email": "robert.marley@example.com",
            "password": "password123"
        })
        self.assertEqual(update_resp.status_code, 200)

        get_resp = self.client.get(f'/api/v1/users/{user_id}')
        data = get_resp.get_json()
        self.assertEqual(data["first_name"], "Robert")
        self.assertEqual(data["email"], "robert.marley@example.com")

    def test_get_all_users(self):
        users_to_create = [
            {"first_name": "User1",
             "last_name": "One",
             "email": "user1@example.com",
             "password": "password123"},
            {"first_name": "User2",
             "last_name": "Two",
             "email": "user2@example.com",
             "password": "password123"}
        ]

        for u in users_to_create:
            resp = self.client.post('/api/v1/users/', json=u)
            self.assertEqual(resp.status_code, 201)

        get_resp = self.client.get('/api/v1/users/')
        self.assertEqual(get_resp.status_code, 200)
        data = get_resp.get_json()
        emails = [user["email"] for user in data]
        for u in users_to_create:
            self.assertIn(u["email"], emails)


class TestUserPassword(unittest.TestCase):
    """Tests pour la gestion des mots de passe dans le modèle User"""

    def setUp(self):
        # On vide la liste globale des emails avant chaque test
        User.emails = set()

    def test_password_hash_and_verify(self):
        """Vérifie que le mot de passe est haché et vérifié correctement"""
        user = User(
            first_name="Alice",
            last_name="Smith",
            email="alice@example.com",
            password="monmotdepasse123"
        )

        # Le mot de passe stocké ne doit pas être en clair
        self.assertNotEqual(user.password, "monmotdepasse123")
        self.assertTrue(user.password.startswith("$2b$")
                        or user.password.startswith("$2a$"))

        # Vérifie que la vérification fonctionne
        self.assertTrue(user.verify_password("monmotdepasse123"))
        self.assertFalse(user.verify_password("motfaux"))

    def test_unique_email(self):
        """Vérifie que deux utilisateurs ne peuvent pas avoir le même email"""
        _ = User("Bob", "Jones", "bob@example.com")
        with self.assertRaises(ValueError):
            _ = User("Bobby", "Brown", "bob@example.com")


class TestUserAuth(unittest.TestCase):

    def setUp(self):
        self.app = create_app('development')
        self.client = self.app.test_client()
        self.facade = HBnBFacade()

        # Crée un utilisateur de test
        self.user = self.facade.create_user({
            "first_name": "Penelope",
            "last_name": "Garcia",
            "email": "The_Black_Queen@FBI.com"
        }, password="MyPAssword")

    def test_login_and_jwt(self):
        # Login
        response = self.client.post('/api/v1/auth/login', json={
            "email": "The_Black_Queen@FBI.com",
            "password": "MyPAssword"
        })

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("access_token", data)

        # Vérifie le JWT
        token_data = decode_token(data["access_token"])
        self.assertEqual(token_data["sub"], str(self.user.id))
        self.assertFalse(token_data["is_admin"])

    def test_login_invalid_credentials(self):
        response = self.client.post('/api/v1/auth/login', json={
            "email": "The_Black_Queen@FBI.com",
            "password": "WrongPassword"
        })
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data["error"], "Invalid credentials")

    def test_access_protected_route(self):
        login_resp = self.client.post('/api/v1/auth/login', json={
            "email": "The_Black_Queen@FBI.com",
            "password": "MyPAssword"
        })
        token = login_resp.get_json()["access_token"]
        protected_resp = self.client.get(
            '/api/v1/auth/protected',
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(protected_resp.status_code, 200)
        data = protected_resp.get_json()
        self.assertIn(str(self.user.id), data["message"])


if __name__ == "__main__":
    unittest.main()
