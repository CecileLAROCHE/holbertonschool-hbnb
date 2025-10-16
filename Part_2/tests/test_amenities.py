from app import create_app


def test_create_valid_amenity():
    app = create_app()
    client = app.test_client()

    response = client.post('/api/v1/amenities/', json={
        "name": "WiFi"
    })

    assert response.status_code == 201


def test_create_invalid_amenity_empty_name():
    app = create_app()
    client = app.test_client()

    response = client.post('/api/v1/amenities/', json={
        "name": ""
    })

    assert response.status_code == 400
    data = response.get_json()
    assert data == {"error": "name is required"}


def test_get_amenities_list():
    app = create_app()
    client = app.test_client()

    response = client.get('/api/v1/amenities/')
    assert response.status_code == 200
