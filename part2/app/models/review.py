from app.models.base_model import BaseModel
from app.persistence.repository import InMemoryRepository


class Review(BaseModel):
    user_repo = InMemoryRepository()
    place_repo = InMemoryRepository()

    def __init__(self, rating, text, user_id, place_id):
        super().__init__()
        if not text:
            raise ValueError("text is required")
        if not (1 <= rating <= 5):
            raise ValueError("rating must be between 1 and 5")
        if place_id is None:
            raise ValueError("place must be provided")
        if not Review.place_repo.get(place_id):
            raise ValueError("place_id must reference a valid Place")
        if user_id is None:
            raise ValueError("user must be provided")
        if not Review.user_repo.get(user_id):
            raise ValueError("valid user_id must reference an existing User")

        self.rating = rating
        self.text = text
        self.user_id = user_id
        self.place_id = place_id

    def to_dict(self):
        """
        Transforme l'objet Review en dictionnaire JSON-serializable.
        Les datetimes sont convertis en chaînes ISO 8601.
        """
        return {
            "id": self.id,
            "rating": self.rating,
            "text": self.text,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at
            else None,
        }
