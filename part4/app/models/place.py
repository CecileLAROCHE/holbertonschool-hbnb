from typing import TYPE_CHECKING
from app.models.base import BaseModel
from sqlalchemy.orm import validates
from app.extensions import db

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.review import Review
    from app.models.amenity import Amenity


class Place(BaseModel):

    __tablename__ = 'places'

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    owner = db.relationship("User", back_populates="places")

    reviews = db.relationship("Review", back_populates="place", cascade="all, delete-orphan")
    amenities = db.relationship("Amenity", secondary="place_amenity", back_populates="places")

    # Champ image principale
    image = db.Column(db.String(255), nullable=True)

    def __init__(
        self, title, price, latitude, longitude, owner, description=""
    ):
        super().__init__()
        self.title: str = title
        self.description: str = description
        self.price: float = price
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.owner: User = owner
        self.reviews: list['Review'] = []
        self.amenities: list['Amenity'] = []

    # ----------------------------------------------------------------------
    # 🔥 VERSION FIXÉE : PAS DE RECURSION, PAS D’APPEL à super().to_dict()
    # ----------------------------------------------------------------------
    def to_dict(self, excluded_attr=None, _visited=None, include_relationships=True):
        if excluded_attr is None:
            excluded_attr = []
        if _visited is None:
            _visited = set()
        if id(self) in _visited:
            return {"id": self.id}
        _visited.add(id(self))

        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "owner_id": self.owner_id,
            "image_url": self.image.replace("static/", "") if self.image else "../assets/default_place.png",
            "average_rating": self.average_rating,
        }

        # --- Owner ---
        if include_relationships and self.owner:
            data["owner"] = {
                "id": self.owner.id,
                "first_name": self.owner.first_name,
                "last_name": self.owner.last_name,
            }
        else:
            data["owner"] = None

        # --- Amenities ---
        if include_relationships:
            data["amenities"] = [
                {"id": a.id, "name": a.name}
                for a in self.amenities
            ]
        else:
            data["amenities"] = []

        # --- Reviews (pas de récursion place → review → place) ---
        if include_relationships:
            data["reviews"] = [
                {
                    "id": r.id,
                    "rating": r.rating,
                    "text": r.text,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                    "user_id": r.user_id,
                    "user": {
                        "id": r.user.id,
                        "first_name": r.user.first_name,
                        "last_name": r.user.last_name,
                    } if r.user else None,
                }
                for r in self.reviews
            ]
        else:
            data["reviews"] = []

        return data

    # ----------------------------------------------------------------------
    # VALIDATIONS
    # ----------------------------------------------------------------------

    @validates("title")
    def validate_title(self, key, title):
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if not title or len(title) > 50:
            raise ValueError("title cannot be empty and must be less than 50 characters")
        return title

    @validates("description")
    def validate_description(self, key, description):
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        if description and len(description) > 500:
            raise ValueError("description must be less than 500 characters")
        return description

    @validates("owner")
    def validate_owner(self, key, owner):
        from app.models.user import User
        if not isinstance(owner, User):
            raise ValueError("owner must be a User instance")
        return owner

    @validates("price")
    def validate_price(self, key, price):
        if not isinstance(price, (int, float)):
            raise TypeError("price must be an int or float")
        if price < 0:
            raise ValueError("price must be a positive number")
        return price

    @validates("latitude")
    def validate_latitude(self, key, latitude):
        if not isinstance(latitude, (int, float)):
            raise TypeError("latitude must be an int or float")
        if latitude < -90 or latitude > 90:
            raise ValueError("latitude must be between -90 and 90")
        return latitude

    @validates("longitude")
    def validate_longitude(self, key, longitude):
        if not isinstance(longitude, (int, float)):
            raise TypeError("longitude must be an int or float")
        if longitude < -180 or longitude > 180:
            raise ValueError("longitude must be between -180 and 180")
        return longitude

    # ----------------------------------------------------------------------
    # Average Rating
    # ----------------------------------------------------------------------
    @property
    def average_rating(self):
        if not self.reviews:
            return None
        return sum(review.rating for review in self.reviews) / len(self.reviews)
