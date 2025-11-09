from app.models.place import Place
from app import db


class PlaceRepository:
    def add(self, place: Place):
        """Ajoute une place dans la base"""
        db.session.add(place)
        db.session.commit()
        return place

    def get_all(self):
        return Place.query.all()

    def get_by_id(self, id):
        return Place.query.get(id)

    def update(self, id, data):
        place = self.get_by_id(id)
        if not place:
            return None
        for key, value in data.items():
            setattr(place, key, value)
        db.session.commit()
        return place

    def delete(self, id):
        place = self.get_by_id(id)
        if not place:
            return None
        db.session.delete(place)
        db.session.commit()
        return place
