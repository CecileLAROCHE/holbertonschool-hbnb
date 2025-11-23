from app.extensions import db
import uuid
from datetime import datetime
from typing import List


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()
        db.session.commit()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self, excluded_attr: List[str] = None, _visited=None, include_relationships: bool = True):
        if excluded_attr is None:
            excluded_attr = []
        if _visited is None:
            _visited = set()

        result = {}

        # Empêche les cycles infinis
        obj_id = id(self)
        if obj_id in _visited:
            return {"id": self.id}
        _visited.add(obj_id)

        # Colonnes simples
        for column in self.__table__.columns:
            if column.name not in excluded_attr:
                value = getattr(self, column.name)
                if isinstance(value, datetime):  # ⭐ Correction !
                    result[column.name] = value.isoformat()
                else:
                    result[column.name] = value

        if include_relationships:
            for rel in self.__mapper__.relationships:
                if rel.key not in excluded_attr:
                    value = getattr(self, rel.key)
                    if value is None:
                        result[rel.key] = None
                    elif isinstance(value, list):
                        result[rel.key] = [item.to_dict(excluded_attr, _visited, False) for item in value]
                    else:
                        result[rel.key] = value.to_dict(excluded_attr, _visited, False)

        return result
