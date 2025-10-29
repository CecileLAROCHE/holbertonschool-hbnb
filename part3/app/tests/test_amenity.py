import pytest
import unittest
from app import create_app
from app.models.amenity import Amenity
from app.api.v1.amenities import amenity_repo


# ------------------- TESTS UNITAIRES DU MODÈLE ------------------- #
class TestAmenityModel(unittest.TestCase):
    """Tests directs sur la classe Amenity"""

    def test_amenity_creation(self):
        amenity = Amenity(name="Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")

    def test_amenity_max_length(self):
        with self.assertRaises(ValueError) as context:
            Amenity(name="a" * 51)
        self.assertEqual(str(context.exception),
                         "Name must be 50 characters max.")

    def test_amenity_missing_field(self):
        with self.assertRaises(TypeError):
            Amenity()

    def test_amenity_update(self):
        amenity = Amenity(name="Wi-Fi")
        new_data = {'name': "Wi-fi"}
        amenity.update(new_data)
        self.assertEqual(amenity.to_dict(), {'id': amenity.id,
                                             'name': "Wi-fi"})

    def test_amenity_update_fail(self):
        amenity = Amenity(name="Wi-Fi")
        with self.assertRaises(ValueError) as context:
            amenity.name = "x" * 51
        self.assertEqual(str(context.exception),
                         "Name must be 50 characters max.")


# ------------------- FIXTURES POUR TESTS API ------------------- #
@pytest.fixture
def client():
    """Fixture Flask client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_repo():
    """Vide le repo avant chaque test"""
    amenity_repo._storage.clear()


# ------------------- TESTS API ------------------- #

def test_create_valid_amenity(client):
    response = client.post('/api/v1/amenities/', json={"name": "Pool"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Pool"
    assert "id" in data


def test_create_invalid_amenity_empty_name(client):
    response = client.post('/api/v1/amenities/', json={"name": ""})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_get_amenity_by_id(client):
    post_resp = client.post('/api/v1/amenities/', json={"name": "WiFi"})
    amenity_id = post_resp.get_json()["id"]

    get_resp = client.get(f'/api/v1/amenities/{amenity_id}')
    assert get_resp.status_code == 200
    data = get_resp.get_json()
    assert data["name"] == "WiFi"


def test_update_amenity(client):
    post_resp = client.post('/api/v1/amenities/', json={"name": "Breakfast"})
    amenity_id = post_resp.get_json()["id"]

    put_resp = client.put(f'/api/v1/amenities/{amenity_id}',
                          json={"name": "Full Breakfast"})
    assert put_resp.status_code == 200
    data = put_resp.get_json()
    assert data["name"] == "Full Breakfast"


def test_duplicate_amenity_name(client):
    # Création de la première amenity
    resp1 = client.post('/api/v1/amenities/', json={"name": "Sauna"})
    assert resp1.status_code == 201

    # Tentative de doublon
    resp2 = client.post('/api/v1/amenities/', json={"name": "Sauna"})
    assert resp2.status_code == 400
    data = resp2.get_json()
    assert "error" in data
    assert ("already exists" in data["error"]
            or "duplicate" in data["error"].lower())


def test_amenity_empty(client):
    response = client.post('/api/v1/amenities/', json={"name": ""})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_amenity_too_long(client):
    long_name = "A" * 51
    response = client.post('/api/v1/amenities/', json={"name": long_name})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_get_amenities(client):
    post_resp = client.post('/api/v1/amenities/', json={"name": "Sauna"})
    assert post_resp.status_code == 201
    amenity_id = post_resp.get_json()["id"]

    get_resp = client.get(f'/api/v1/amenities/{amenity_id}')
    assert get_resp.status_code == 200
    data = get_resp.get_json()
    assert isinstance(data, dict)
    assert data["id"] == amenity_id
    assert data["name"] == "Sauna"


def test_get_all_amenities(client):
    client.post('/api/v1/amenities/', json={"name": "Gym"})
    client.post('/api/v1/amenities/', json={"name": "Spa"})
    resp = client.get('/api/v1/amenities/')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) >= 2
    assert any(a["name"] == "Gym" for a in data)
    assert any(a["name"] == "Spa" for a in data)
