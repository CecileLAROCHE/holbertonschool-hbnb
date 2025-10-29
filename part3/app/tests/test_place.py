import pytest
from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review


# ---------- TESTS UNITAIRES DIRECTS (modèle) ----------

def test_place_creation_model():
    """Test direct de création de Place (sans API)"""
    owner = User(first_name="Alice",
                 last_name="Smith",
                 email="alice.smith@example.com")

    place = Place(title="Cozy Apartment",
                  description="A nice place to stay",
                  price=100.0,
                  latitude=37.7749,
                  longitude=-122.4194,
                  owner=owner)

    assert place.title == "Cozy Apartment"
    assert place.price == 100.0
    assert place.latitude == 37.7749
    assert place.longitude == -122.4194
    assert place.owner == owner
    assert place.description == "A nice place to stay"

    # Ajout d’un avis
    review = Review(text="Great stay!", rating=5, place=place, user=owner)
    place.add_review(review)
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"


def test_place_invalid_title():
    """Test : titre vide ou invalide"""
    owner = User(first_name="Bob", last_name="Lee", email="bob@example.com")

    with pytest.raises(ValueError):
        Place(title="", price=50.0, latitude=48.8, longitude=2.3, owner=owner)

    with pytest.raises(TypeError):
        Place(title=123, price=50.0, latitude=48.8, longitude=2.3, owner=owner)


def test_place_invalid_price():
    owner = User(first_name="Lara",
                 last_name="Croft",
                 email="lara@example.com")

    with pytest.raises(TypeError):
        Place(title="Cottage",
              price="cheap",
              latitude=48.8, longitude=2.3, owner=owner)

    with pytest.raises(ValueError):
        Place(title="Cottage", price=-10,
              latitude=48.8,
              longitude=2.3,
              owner=owner)


def test_place_invalid_latitude_longitude():
    owner = User(first_name="Tom", last_name="Hardy", email="tom@example.com")

    with pytest.raises(TypeError):
        Place(title="House",
              price=100,
              latitude="48.8",
              longitude=2.3,
              owner=owner)

    with pytest.raises(ValueError):
        Place(title="House",
              price=100,
              latitude=200,
              longitude=2.3,
              owner=owner)

    with pytest.raises(ValueError):
        Place(title="House",
              price=100,
              latitude=48.8,
              longitude=-200, owner=owner)


def test_owner_type():
    """Vérifie que owner doit être une instance de User"""
    with pytest.raises(TypeError):
        Place(title="Loft",
              price=100,
              latitude=48.8,
              longitude=2.3,
              owner="not_user")


# ---------- FIXTURES API FLASK ----------

@pytest.fixture
def owner():
    return User(first_name="Dereck",
                last_name="Morgan",
                email="M.Dereck@FBI.com")


@pytest.fixture
def place_payload(owner):
    """Payload template pour API"""
    return {
        "title": "Cozy Cottage",
        "description": "A small cozy place",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "price": 100,
        "owner_id": owner.id,
    }


@pytest.fixture
def client():
    """Client Flask pour tests d’API"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ---------- TESTS API ----------

def test_create_valid_place(client, owner, place_payload):
    response = client.post('/api/v1/places/', json=place_payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == place_payload['title']
    assert data['owner_id'] == owner.id


def test_create_invalid_place_empty_title(client, owner, place_payload):
    place_payload['title'] = ""
    response = client.post('/api/v1/places/', json=place_payload)
    assert response.status_code == 400


def test_get_place_by_id(client, owner, place_payload):
    post_resp = client.post('/api/v1/places/', json=place_payload)
    place_id = post_resp.get_json()["id"]

    get_resp = client.get(f'/api/v1/places/{place_id}')
    assert get_resp.status_code == 200
    data = get_resp.get_json()
    assert data['id'] == place_id


def test_update_place(client, owner, place_payload):
    post_resp = client.post('/api/v1/places/', json=place_payload)
    place_id = post_resp.get_json()["id"]

    updated_payload = place_payload.copy()
    updated_payload['price'] = 150

    put_resp = client.put(f'/api/v1/places/{place_id}', json=updated_payload)
    assert put_resp.status_code == 200
    data = put_resp.get_json()
    assert data['price'] == 150


def test_get_all_places(client, owner, place_payload):
    payload1 = place_payload.copy()
    payload1['title'] = "Place 1"
    client.post('/api/v1/places/', json=payload1)

    payload2 = place_payload.copy()
    payload2['title'] = "Place 2"
    client.post('/api/v1/places/', json=payload2)

    resp = client.get('/api/v1/places/')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) >= 2


def test_invalid_fields(client, place_payload):
    """Tests combinés pour tous les champs invalides"""
    # titre vide
    place_payload['title'] = ""
    assert client.post('/api/v1/places/',
                       json=place_payload).status_code == 400

    # titre trop long
    place_payload['title'] = "x" * 101
    assert client.post('/api/v1/places/',
                       json=place_payload).status_code == 400

    # prix vide
    place_payload['price'] = ""
    assert client.post('/api/v1/places/',
                       json=place_payload).status_code == 400

    # prix non numérique
    place_payload['price'] = "abc"
    assert client.post('/api/v1/places/',
                       json=place_payload).status_code == 400

    # prix négatif
    place_payload['price'] = -10
    assert client.post('/api/v1/places/',
                       json=place_payload).status_code == 400

    # latitude hors bornes
    place_payload['latitude'] = 200
    assert client.post('/api/v1/places/',
                       json=place_payload).status_code == 400

    # longitude hors bornes
    place_payload['longitude'] = -200
    assert client.post('/api/v1/places/',
                       json=place_payload).status_code == 400
