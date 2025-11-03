from app import db
from app.models.user import User

class UserRepository:
    def add(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def get(self, user_id):
        return User.query.get(user_id)

    def get_all(self):
        return User.query.all()

    def update(self, user_id, data):
        user = self.get(user_id)
        if not user:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    def delete(self, user_id):
        user = self.get(user_id)
        if not user:
            return None
        db.session.delete(user)
        db.session.commit()
        return user

    def get_by_attribute(self, attr_name, value):
        return User.query.filter(getattr(User, attr_name) == value).first()
