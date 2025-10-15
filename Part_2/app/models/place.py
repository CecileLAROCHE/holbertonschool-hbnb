from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        if not title or len(title) > 100:
            raise ValueError("title must be 1-100 characters")
        if not price > 0:
            raise ValueError("must be positive")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("latitude must be between -90.0 and 90.0")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("longitude must be between -180.0 and 180.0")
        if not isinstance(owner, User):
            raise TypeError("owner must be a User instance")
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
