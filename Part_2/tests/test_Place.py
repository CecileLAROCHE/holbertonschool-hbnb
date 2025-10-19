import pytest
from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review


def test_place_creation():
    user = User(first_name="Alice",
                last_name="Smith",
                email="alice.smith@example.com")
    place = Place(title="Cozy Apartment",
                  description="A nice place to stay",
                  price=100,
                  latitude=37.7749,
                  longitude=-122.4194,
                  owner_id=user.id)

    review = Review(text="Great stay!",
                    rating=5,
                    user_id=user.id,
                    place_id=place.id)
    place.add_review(review)

    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    print("Place creation and relationship test passed!")


@pytest.fixture
def owner():
    user = User(first_name="Dereck",
                last_name="Morgan",
                email="M.Dereck@FBI.com")
    return user


def test_review_creation():
    user = User(first_name="John",
                last_name="Doe",
                email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    print("User creation test passed!")


@pytest.fixture
def place_payload(owner):
    """Payload template for creating a place"""
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
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


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


def test_title_empty(client, place_payload):
    place_payload['title'] = ""
    response = client.post('/api/v1/places/', json=place_payload)
    assert response.status_code == 400


def test_title_to_long(client, place_payload):
    place_payload['title'] = "x" * 101
    response = client.post('/api/v1/places/', json=place_payload)
    assert response.status_code == 400


def test_price_empty(client, place_payload):
    place_payload['price'] = ""
    response = client.post('/api/v1/places/', json=place_payload)
    assert response.status_code == 400


def test_price_not_number(client, place_payload):
    place_payload['price'] = "str"
    response = client.post('/api/v1/places/', json=place_payload)
    assert response.status_code == 400


def test_price_positive_number(client, place_payload):
    place_payload['price'] = -10
    response = client.post('/api/v1/places/', json=place_payload)
    assert response.status_code == 400


def test_latitude_empty(client, place_payload):
    place_payload['latitude'] = ""
    response = client.post('/api/v1/places/', json=place_payload)
    assert response.status_code == 400


def test_latitude_below_minimum(client, place_payload):
    place_payload['latitude'] = -200
    response = client.post('/api/v1/places/', json=place_payload)
    assert response.status_code == 400


def test_latitude_above_maximum(client, place_payload):
    place_payload['latitude'] = 200
    response = client.post('/api/v1/places/', json=place_payload)
    assert response.status_code == 400


def test_longitude_empty(client, place_payload):
    place_payload['longitude'] = ""
    response = client.post('/api/v1/places/', json=place_payload)
    assert response.status_code == 400


def test_longitude_below_minimum(client, place_payload):
    place_payload['longitude'] = -200
    response = client.post('/api/v1/places/', json=place_payload)
    assert response.status_code == 400


def test_longitude_above_maximum(client, place_payload):
    place_payload['longitude'] = 200
    response = client.post('/api/v1/places/', json=place_payload)
    assert response.status_code == 400
