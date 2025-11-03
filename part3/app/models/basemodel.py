import uuid
from datetime import datetime as dt
from app import db


class BaseModel(db.Model):
    """Base model for all SQLAlchemy entities."""
    __abstract__ = True

    id = db.Column(db.String(36),
                   primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=dt.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=dt.utcnow, onupdate=dt.utcnow)

    def save(self):
        """Save the current object to the database."""
        self.updated_at = dt.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update fields from a dictionary and commit."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = dt.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current object from the database."""
        db.session.delete(self)
        db.session.commit()

    def is_max_length(self, name, value, max_length):
        """Check that a string does not exceed max_length."""
        if len(value) > max_length:
            raise ValueError(f"{name} must be ≤ {max_length} characters.")

    def is_between(self, name, value, min_val, max_val):
        """Check that a numeric value is within range."""
        if not min_val <= value <= max_val:
            raise ValueError(
                f"{name} must be between {min_val} and {max_val}."
            )
