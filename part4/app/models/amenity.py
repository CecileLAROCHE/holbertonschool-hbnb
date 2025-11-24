from typing import TYPE_CHECKING
from app.models.base import BaseModel
from sqlalchemy.orm import validates
from app.extensions import db

if TYPE_CHECKING:
    from app.models.place import Place

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    # On met le nom du modèle en string pour éviter la dépendance circulaire
    places = db.relationship("Place", secondary="place_amenity", back_populates="amenities")

    def __init__(self, name) -> None:
        super().__init__()
        self.name: str = name

    @validates("name")
    def validate_name(self, key, value: str):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if not value or len(value) > 50:
            raise ValueError(
                "Name cannot be empty and must be less than 50 characters"
            )
        return value


class PlaceAmenity(db.Model):
    __tablename__ = "place_amenity"
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), primary_key=True)
    amenity_id = db.Column(db.String(36), db.ForeignKey("amenities.id"), primary_key=True)

    def __init__(self, place: 'Place', amenity: 'Amenity') -> None:
        self.place: 'Place' = place
        self.amenity: 'Amenity' = amenity
