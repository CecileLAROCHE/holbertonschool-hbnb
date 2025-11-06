from .basemodel import BaseModel, db


class Review(BaseModel):
    __tablename__ = "reviews"

    _text = db.Column("text", db.String(500), nullable=False)
    _rating = db.Column("rating", db.Integer, nullable=False)

    place_id = db.Column(db.String(36),
                         db.ForeignKey("places.id"), nullable=False)
    user_id = db.Column(db.String(36),
                        db.ForeignKey("users.id"), nullable=False)

    place = db.relationship("Place", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise TypeError("Text must be a string")
        if not value.strip():
            raise ValueError("Text cannot be empty")
        self._text = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        super().is_between("Rating", value, 1, 6)
        self._rating = value

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id
        }
