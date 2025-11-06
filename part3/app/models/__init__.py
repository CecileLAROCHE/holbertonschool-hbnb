# --------------------------
# Imports
# --------------------------
from app import db
from .user import User  # noqa: F401
from .place import Place  # noqa: F401
from .amenity import Amenity  # noqa: F401
from .review import Review  # noqa: F401

# --------------------------
# Table d'association Place ↔ Amenity
# --------------------------
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id',
              db.String(36),
              db.ForeignKey('places.id'),
              primary_key=True),
    db.Column('amenity_id',
              db.String(36),
              db.ForeignKey('amenities.id'),
              primary_key=True)
)
