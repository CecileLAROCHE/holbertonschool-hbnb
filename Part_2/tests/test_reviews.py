from app.models.user import User
from app.models.place import Place
from app.models.review import Review


def test_review_creation():
    user = User(first_name="John",
                last_name="Doe",
                email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value
    print("User creation test passed!")


def test_place_creation():
    # Crée un utilisateur pour le lien
    user = User(first_name="John", last_name="Doe", email="john@example.com")

    # Crée un lieu associé à l'utilisateur
    place = Place(title="Cozy Apartment",
                  description="A nice place to stay",
                  price=100,
                  latitude=37.7749,
                  longitude=-122.4194,
                  owner_id=user.id)

    # Crée une review associée à l'utilisateur et au lieu
    review = Review(text="Great stay!",
                    rating=5,
                    user_id=user.id,
                    place_id=place.id,)

    assert review.text == "Great stay!"
    assert review.rating == 5
    assert review.user_id == user.id
    assert review.place_id == place.id

    print("Review creation test passed!")
