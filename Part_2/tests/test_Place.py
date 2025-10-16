from app.models.place import Place
from app.models.user import User
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

    # Adding a review
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


test_place_creation()
