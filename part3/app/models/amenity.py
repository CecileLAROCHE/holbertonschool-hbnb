from .basemodel import BaseModel, db


class Amenity(BaseModel):
    __tablename__ = "amenities"

    _name = db.Column("name", db.String(50), nullable=False, unique=True)

    places = db.relationship(
        "Place", secondary="place_amenity", back_populates="amenities"
    )

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value.strip():
            raise ValueError("Name cannot be empty")
        super().is_max_length("Name", value, 50)
        self._name = value

    def to_dict(self):
        return {"id": self.id, "name": self.name}
