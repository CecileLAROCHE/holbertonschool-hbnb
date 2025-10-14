from app.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, rating, text, place, user):
        super().__init__()
        if not text:
            raise ValueError("text is required")
        if not (1 <= rating <= 5):
            raise ValueError("rating must be between 1 and 5")
        if place is None:
            raise ValueError("place must be provided")
        if user is None:
            raise ValueError("user must be provided")
        self.rating = rating
        self.text = text
        self.place = place
        self.user = user
