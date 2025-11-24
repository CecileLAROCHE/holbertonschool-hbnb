from app.extensions import db
from typing import TYPE_CHECKING
from app.models.base import BaseModel
from sqlalchemy.orm import validates

if TYPE_CHECKING:
    from app.models.place import Place
    from app.models.user import User


class Review(BaseModel):

    __tablename__ = 'reviews'

    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)

    user = db.relationship("User", back_populates="reviews")
    place = db.relationship("Place", back_populates="reviews")

    def __init__(self, text, rating, place, user) -> None:
        super().__init__()
        self.text: str = text
        self.rating: int = rating
        self.place: 'Place' = place
        self.user: 'User' = user

    # ----------------------------
    # VALIDATIONS
    # ----------------------------
    @validates("text")
    def validate_text(self, key, text):
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if not text or len(text) > 500:
            raise ValueError("text cannot be empty and must be less than 500 characters")
        return text

    @validates("rating")
    def validate_rating(self, key, rating):
        if not isinstance(rating, (int, float)):
            raise TypeError("rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")
        return rating

    @validates("place")
    def validate_place(self, key, place):
        from app.models.place import Place
        if not isinstance(place, Place):
            raise ValueError("place must be a Place instance")
        return place

    @validates("user")
    def validate_user(self, key, user):
        from app.models.user import User
        if not isinstance(user, User):
            raise ValueError("user must be a User instance")
        return user

    # ----------------------------
    # SAFE to_dict() pour éviter récursion
    # ----------------------------
    def to_dict(self, _visited=None, include_relationships=True):
        if _visited is None:
            _visited = set()
        if id(self) in _visited:
            return {"id": self.id}
        _visited.add(id(self))

        data = {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "place_title": None  # valeur par défaut
        }

        if include_relationships:
            # User info
            if self.user:
                data["user"] = {
                    "id": self.user.id,
                    "first_name": self.user.first_name,
                    "last_name": self.user.last_name,
                    "email": getattr(self.user, "email", None)
                }
            else:
                data["user"] = None

            # Place title rapide
            if self.place_id:
                from app.models.place import Place
                place = Place.query.get(self.place_id)
                data["place_title"] = place.title if place else "Unknown"

        return data
