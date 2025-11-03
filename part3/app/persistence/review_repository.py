from app.models.review import Review
from app import db


class ReviewRepository:
    def create(self, data):
        review = Review(**data)
        db.session.add(review)
        db.session.commit()
        return review

    def get_all(self):
        return Review.query.all()

    def get_by_id(self, id):
        return Review.query.get(id)

    def update(self, id, data):
        review = self.get_by_id(id)
        if not review:
            return None
        for key, value in data.items():
            setattr(review, key, value)
        db.session.commit()
        return review

    def delete(self, id):
        review = self.get_by_id(id)
        if not review:
            return None
        db.session.delete(review)
        db.session.commit()
        return review
