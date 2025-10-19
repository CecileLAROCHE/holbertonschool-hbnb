import unittest
from app import create_app
from app.models.user import User


def test_user_creation():
    user = User(first_name="John",
                last_name="Doe",
                email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    print("User creation test passed!")


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_create_valid_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_user_bad_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data, {"error": "Invalid email format"})

    def test_get_user_by_id(self):
        create_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Wonder",
            "email": "alice@example.com"
        })
        self.assertEqual(create_resp.status_code, 201)
        user_id = create_resp.get_json()["id"]

        get_resp = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(get_resp.status_code, 200)
        data = get_resp.get_json()
        self.assertEqual(data["email"], "alice@example.com")

    def test_update_user(self):
        create_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Marley",
            "email": "bob@example.com"
        })
        self.assertEqual(create_resp.status_code, 201)
        user_id = create_resp.get_json()["id"]

        update_resp = self.client.put(f'/api/v1/users/{str(user_id)}', json={
            "first_name": "Robert",
            "last_name": "Marley",
            "email": "robert.marley@example.com"
        })
        self.assertEqual(update_resp.status_code, 200)

        get_resp = self.client.get(f'/api/v1/users/{user_id}')
        data = get_resp.get_json()
        self.assertEqual(data["first_name"], "Robert")
        self.assertEqual(data["email"], "robert.marley@example.com")

    def test_get_all_users(self):
        # Crée quelques utilisateurs pour tester la liste
        users_to_create = [
            {"first_name": "User1",
             "last_name": "One",
             "email": "user1@example.com"},
            {"first_name": "User2",
             "last_name": "Two",
             "email": "user2@example.com"}
        ]

        for u in users_to_create:
            resp = self.client.post('/api/v1/users/', json=u)
            self.assertEqual(resp.status_code, 201)

        # Récupère la liste complète des utilisateurs
        get_resp = self.client.get('/api/v1/users/')
        self.assertEqual(get_resp.status_code, 200)
        data = get_resp.get_json()

        # Vérifie que tous les utilisateurs créés sont présents dans la liste
        emails = [user["email"] for user in data]
        for u in users_to_create:
            self.assertIn(u["email"], emails)

        print("Récupération liste complète test passed!")
