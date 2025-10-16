import pytest
from app import create_app
from app.api.v1.amenities import amenity_repo


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_repo():
    amenity_repo._storage.clear()


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


def test_get_all_amenities(client):
    client.post('/api/v1/amenities/', json={"name": "Gym"})
    client.post('/api/v1/amenities/', json={"name": "Spa"})
    resp = client.get('/api/v1/amenities/')
    data = resp.get_json()
    assert resp.status_code == 200
    assert len(data) == 2
    assert any(a["name"] == "Gym" for a in data)
    assert any(a["name"] == "Spa" for a in data)


def test_duplicate_amenity_name(client):
    # Création de la première amenity
    resp1 = client.post('/api/v1/amenities/', json={"name": "Sauna"})
    assert resp1.status_code == 201

    resp2 = client.post('/api/v1/amenities/', json={"name": "Sauna"})

    assert resp2.status_code == 400
    data = resp2.get_json()
    assert "error" in data
    assert (
        "already exists" in data["error"]
        or "duplicate" in data["error"].lower()
    )
