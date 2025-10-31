import pytest
from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.services.facade import HBnBFacade
facade = HBnBFacade()

# ---------------- FIXTURES ----------------


def app_client():
    """Client Flask pour tests d’API"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def owner():
    """Crée un utilisateur pour les tests API"""
    # On initialise l'email set pour ne pas avoir de doublon
    User.emails = set()

    user = User(
        first_name="Dereck",
        last_name="Morgan",
        email="M.Dereck@FBI.com",
        password="SuperSecret123"  # Mot de passe pour login
    )
    return user


@pytest.fixture
def auth_header(app_client, owner):
    """Fixture pour obtenir le header Authorization avec JWT"""
    # Login pour obtenir le token JWT
    resp = app_client.post('/api/v1/auth/login', json={
        "email": owner.email,
        "password": "SuperSecret123"  # Mot de passe en clair
    })
    data = resp.get_json()
    assert "access_token" in data, f"Login failed, got {data}"
    token = data["access_token"]
    return {"Authorization": f"Bearer {token}"}


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

# -------------------- TESTS UNITAIRES DIRECTS (MODÈLE) --------------------


def test_place_creation_model():
    """Test direct de création de Place (sans API)"""
    owner = User(first_name="Alice",
                 last_name="Smith",
                 email="alice.smith@example.com")

    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100.0,
        latitude=37.7749,
        longitude=-122.4194,
        owner_id=owner.id
    )

    assert place.title == "Cozy Apartment"
    assert place.price == 100.0
    assert place.latitude == 37.7749
    assert place.longitude == -122.4194
    assert place.owner_id == owner.id
    assert place.description == "A nice place to stay"

    # Ajout d’un avis
    review = Review(text="Great stay!", rating=5, place=place, user=owner)
    place.add_review(review)
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"


def test_place_invalid_title():
    owner = User(first_name="Bob", last_name="Lee", email="bob@example.com")

    with pytest.raises(ValueError):
        Place(title="",
              price=50.0, latitude=48.8, longitude=2.3, owner_id=owner.id)

    with pytest.raises(TypeError):
        Place(title=123,
              price=50.0,
              latitude=48.8,
              longitude=2.3,
              owner_id=owner.id)


def test_place_invalid_price():
    owner = User(first_name="Lara",
                 last_name="Croft",
                 email="lara@example.com")

    with pytest.raises(TypeError):
        Place(title="Cottage",
              price="cheap",
              latitude=48.8,
              longitude=2.3,
              owner_id=owner.id)

    with pytest.raises(ValueError):
        Place(title="Cottage",
              price=-10,
              latitude=48.8,
              longitude=2.3,
              owner_id=owner.id)


def test_place_invalid_latitude_longitude():
    owner = User(first_name="Tom", last_name="Hardy", email="tom@example.com")

    with pytest.raises(TypeError):
        Place(title="House",
              price=100,
              latitude="48.8",
              longitude=2.3,
              owner_id=owner.id)

    with pytest.raises(ValueError):
        Place(title="House",
              price=100, latitude=200,
              longitude=2.3,
              owner_id=owner.id)

    with pytest.raises(ValueError):
        Place(title="House",
              price=100,
              latitude=48.8,
              longitude=-200,
              owner_id=owner.id)


def test_owner_type():
    with pytest.raises(TypeError):
        Place(title="Loft", price=100,
              latitude=48.8,
              longitude=2.3,
              owner="not_user")


# -------------------- FIXTURES API FLASK --------------------

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def owner():
    """Crée un utilisateur réel pour les tests API"""
    user_data = {
        "first_name": "Dereck",
        "last_name": "Morgan",
        "email": "M.Dereck@FBI.com",
        "password": "MyPassword123"
    }
    try:
        facade.create_user(**user_data)
    except Exception:
        # Ignore si déjà créé
        pass
    return facade.get_user_by_email(user_data["email"])


@pytest.fixture
def auth_header(client, owner):
    """Fixture pour obtenir le header Authorization avec JWT"""
    resp = client.post('/api/v1/auth/login', json={
        "email": owner.email,
        "password": "MyPassword123"
    })
    token = resp.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


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


# -------------------- TESTS API --------------------

def test_create_valid_place(client, place_payload, auth_header):
    response = client.post('/api/v1/places/',
                           json=place_payload, headers=auth_header)
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == place_payload['title']
    assert data['owner_id'] == place_payload['owner_id']


def test_create_invalid_place_empty_title(client, place_payload, auth_header):
    place_payload['title'] = ""
    response = client.post('/api/v1/places/',
                           json=place_payload, headers=auth_header)
    assert response.status_code == 400


def test_get_place_by_id(client, place_payload, auth_header):
    post_resp = client.post('/api/v1/places/',
                            json=place_payload, headers=auth_header)
    place_id = post_resp.get_json()["id"]

    get_resp = client.get(f'/api/v1/places/{place_id}', headers=auth_header)
    assert get_resp.status_code == 200
    data = get_resp.get_json()
    assert data['id'] == place_id


def test_update_place(client, place_payload, auth_header):
    post_resp = client.post('/api/v1/places/',
                            json=place_payload, headers=auth_header)
    place_id = post_resp.get_json()["id"]

    updated_payload = place_payload.copy()
    updated_payload['price'] = 150

    put_resp = client.put(f'/api/v1/places/{place_id}',
                          json=updated_payload, headers=auth_header)
    assert put_resp.status_code == 200
    data = put_resp.get_json()
    assert data['price'] == 150


def test_get_all_places(client, place_payload, auth_header):
    payload1 = place_payload.copy()
    payload1['title'] = "Place 1"
    client.post('/api/v1/places/', json=payload1, headers=auth_header)

    payload2 = place_payload.copy()
    payload2['title'] = "Place 2"
    client.post('/api/v1/places/', json=payload2, headers=auth_header)

    resp = client.get('/api/v1/places/', headers=auth_header)
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) >= 2


def test_invalid_fields(client, place_payload, auth_header):
    """Tests combinés pour tous les champs invalides"""
    invalid_cases = [
        {"title": ""},  # titre vide
        {"title": "x"*101},  # titre trop long
        {"price": ""},  # prix vide
        {"price": "abc"},  # prix non numérique
        {"price": -10},  # prix négatif
        {"latitude": 200},  # latitude hors bornes
        {"longitude": -200},  # longitude hors bornes
    ]
    for case in invalid_cases:
        payload = place_payload.copy()
        payload.update(case)
        resp = client.post('/api/v1/places/',
                           json=payload, headers=auth_header)
        assert resp.status_code == 400
