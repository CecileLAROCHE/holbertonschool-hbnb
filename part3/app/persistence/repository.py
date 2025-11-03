from abc import ABC, abstractmethod
from sqlalchemy.orm import sessionmaker
from app.persistence.database import engine


Session = sessionmaker(bind=engine)

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    """In-memory repository (used for testing or before DB setup)."""

    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            return obj
        return None

    def delete(self, obj_id):
        return self._storage.pop(obj_id, None)

    def get_by_attribute(self, attr_name, attr_value):
        return next(
            (obj for obj in self._storage.values()
             if getattr(obj, attr_name) == attr_value),
            None
        )


class SQLAlchemyRepository(Repository):
    """Repository implementation using SQLAlchemy ORM."""

    def __init__(self, model_class):
        self.model_class = model_class
        self.session = Session()

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get(self, obj_id):
        return self.session.get(self.model_class, obj_id)

    def get_all(self):
        return self.session.query(self.model_class).all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        self.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            return None
        self.session.delete(obj)
        self.session.commit()
        return obj

    def get_by_attribute(self, attr_name, attr_value):
        return self.session.query(self.model_class).filter(
            getattr(self.model_class, attr_name) == attr_value
        ).first()
