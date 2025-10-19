from app.models.base_model import BaseModel


class Place(BaseModel):
    """Represents a place listed in the HBnB application.

    Inherits from BaseModel and includes additional attributes such as
    title, description, price, location (latitude and longitude), and
    relationships with reviews and amenities.
    """
    def __init__(self, title, description, price, latitude, longitude,
                 owner_id):
        """
        Initialize a new Place instance with validation.

        Args:
            title (str): The title of the place (required, max 100 chars).
            description (str): A short description of the place.
            price (float): The nightly price of the place (must be positive).
            latitude (float): The latitude coordinate (-90.0 to 90.0).
            longitude (float): The longitude coordinate (-180.0 to 180.0).
            owner_id (str): The UUID of the user who owns the place.

        Raises:
            ValueError: If any of the provided fields are invalid.
        """
        super().__init__()

        # --- Input validation ---
        if not title:
            raise ValueError("title is required")
        if len(title) > 100:
            raise ValueError("title must be at most 100 characters")

        if price is None or price == "":
            raise ValueError("price must be a number")
        if not isinstance(price, (int, float)):
            raise ValueError("price must be a number")
        if price < 0:
            raise ValueError("must be positive")

        if latitude is None or latitude == "":
            raise ValueError("latitude must be a number")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("latitude must be between -90.0 and 90.0")
        
        if longitude is None or longitude == "":
            raise ValueError("longitude must be a number")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("longitude must be between -180.0 and 180.0")

        # --- Attribute assignment ---
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id  # Store only the owner's UUID
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """
        Add a review to this place.

        Args:
            review (Review): The review object to be added.
        """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Add an amenity to this place.

        Args:
            amenity (Amenity): The amenity object to be added.
        """
        self.amenities.append(amenity)

    def to_dict(self):
        """
        Add an amenity to this place.

        Args:
            amenity (Amenity): The amenity object to be added.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": self.amenities,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
