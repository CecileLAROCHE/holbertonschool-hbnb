from app.models.amenity import Amenity
from app import db


class AmenityRepository:
    def create(self, data):
        amenity = Amenity(**data)
        db.session.add(amenity)
        db.session.commit()
        return amenity

    def get_all(self):
        return Amenity.query.all()

    def get_by_id(self, id):
        return Amenity.query.get(id)

    def update(self, id, data):
        amenity = self.get_by_id(id)
        if not amenity:
            return None
        for key, value in data.items():
            setattr(amenity, key, value)
        db.session.commit()
        return amenity

    def delete(self, id):
        amenity = self.get_by_id(id)
        if not amenity:
            return None
        db.session.delete(amenity)
        db.session.commit()
        return amenity
