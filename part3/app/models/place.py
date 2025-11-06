from .basemodel import BaseModel, db


class Place(BaseModel):
    __tablename__ = "places"

    _title = db.Column("title", db.String(100), nullable=False)
    _description = db.Column("description", db.Text, nullable=True)
    _price = db.Column("price", db.Float, nullable=False)
    _latitude = db.Column("latitude", db.Float, nullable=False)
    _longitude = db.Column("longitude", db.Float, nullable=False)
    owner_id = db.Column(db.String(36),
                         db.ForeignKey("users.id"), nullable=False)

    # Relations
    reviews = db.relationship(
        "Review",
        back_populates="place",
        cascade="all, delete-orphan",
        lazy=True
    )
    amenities = db.relationship(
        "Amenity",
        secondary="place_amenity",
        back_populates="places",
        lazy=True
    )
    reviews = db.relationship(
        "Review", back_populates="place",
        cascade="all, delete-orphan", lazy=True
    )

# ---- PROPERTIES ----
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if not value.strip():
            raise ValueError("Title cannot be empty")
        super().is_max_length("Title", value, 100)
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be numeric")
        if value < 0:
            raise ValueError("Price must be positive")
        self._price = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("Latitude must be numeric")
        super().is_between("Latitude", value, -90, 90)
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("Longitude must be numeric")
        super().is_between("Longitude", value, -180, 180)
        self._longitude = value

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self._description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id
        }

    def to_dict_list(self):
        return {
            **self.to_dict(),
            "amenities": [a.to_dict() for a in self.amenities],
            "reviews": [r.to_dict() for r in self.reviews]
        }
