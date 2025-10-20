from app.models.user import User
from app.models.place import Place
from app.models.review import Review
import pytest
from app import create_app


def test_revieuw_creation():
    user = User(first_name="John",
                last_name="Doe",
                email="john@example.com")
    place = Place(title="Cozy Apartment",
                  description="A nice place to stay",
                  price=100,
                  latitude=37.7749,
                  longitude=-122.4194,
                  owner_id=user.id)

    Review.user_repo.add(user)
    Review.place_repo.add(place)

    review = Review(text="Great stay!",
                    rating=5,
                    user_id=user.id,
                    place_id=place.id,)

    assert review.text == "Great stay!"
    assert review.rating == 5
    assert review.user_id == user.id
    assert review.place_id == place.id


def test_revieuw_empty_text():
    user = User(first_name="Spencer",
                last_name="Reid",
                email="Spencer@example.com")
    place = Place(title="Cozy house",
                  description="near the desert",
                  price=150,
                  latitude=36.169941,
                  longitude=-115.139830,
                  owner_id=user.id)
    Review.user_repo.add(user)
    Review.place_repo.add(place)
    with pytest.raises(ValueError) as exc_info:
        Review(
            text="",
            rating=4,
            user_id=user.id,
            place_id=place.id,
            )
    assert "text is required" in str(exc_info.value)


def test_review_invalid_user_id():
    # Place valide
    user = User(first_name="Penelope",
                last_name="Garcia",
                email="The_Black_Queen@example.com")
    place = Place(title="Nice house",
                  description="Sunny place",
                  price=200,
                  latitude=37.787994,
                  longitude=-122.407437,
                  owner_id=user.id)
    Review.place_repo.add(place)
    invalid_user_id = "non-existent-user-id"
    with pytest.raises(ValueError) as exc_info:
        Review(
            text="Amazing stay!",
            rating=5,
            user_id=invalid_user_id,
            place_id=place.id
        )
    assert "valid user_id" in str(exc_info.value)


def test_review_invalid_place_id():
    # User valide
    user = User(first_name="Emily",
                last_name="Prentiss",
                email="Prentiss@example.com")
    invalid_place_id = "non-existent-place-id"
    Review.user_repo.add(user)
    with pytest.raises(ValueError) as exc_info:
        Review(
            text="Loved it!",
            rating=4,
            user_id=user.id,
            place_id=invalid_place_id
        )
    assert "place_id must reference a valid Place" in str(exc_info.value)


def test_revieuw_rating_below_minimum():
    user = User(first_name="Spencer",
                last_name="Reid",
                email="Spencer@example.com")
    place = Place(title="Cozy house",
                  description="near the desert",
                  price=150,
                  latitude=36.169941,
                  longitude=-115.139830,
                  owner_id=user.id)
    Review.user_repo.add(user)
    Review.place_repo.add(place)
    with pytest.raises(ValueError) as exc_info:
        Review(
            text="really bad place",
            rating=0,
            user_id=user.id,
            place_id=place.id,
            )
    assert "rating must be between 1 and 5" in str(exc_info.value)


def test_revieuw_rating_above_maximum():
    user = User(first_name="Spencer",
                last_name="Reid",
                email="Spencer@example.com")
    place = Place(title="Cozy house",
                  description="near the desert",
                  price=150,
                  latitude=36.169941,
                  longitude=-115.139830,
                  owner_id=user.id)
    Review.user_repo.add(user)
    Review.place_repo.add(place)
    with pytest.raises(ValueError) as exc_info:
        Review(
            text="Good stay",
            rating=7,
            user_id=user.id,
            place_id=place.id,
            )
    assert "rating must be between 1 and 5" in str(exc_info.value)


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
