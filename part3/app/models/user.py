import re
from .basemodel import BaseModel, db
from app import bcrypt


class User(BaseModel):
    __tablename__ = "users"

    _first_name = db.Column("first_name", db.String(50), nullable=False)
    _last_name = db.Column("last_name", db.String(50), nullable=False)
    _email = db.Column("email", db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    _is_admin = db.Column("is_admin", db.Boolean, default=False)

    # --- 🔗 Relations ---
    places = db.relationship('Place', back_populates='owner', lazy=True)
    reviews = db.relationship('Review', back_populates='author', lazy=True)

    # --- ✅ Validations et propriétés ---
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        super().is_max_length("First name", value, 50)
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        super().is_max_length("Last name", value, 50)
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        self._email = value

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("Is Admin must be boolean")
        self._is_admin = value

    def hash_password(self, password):
        if password:
            self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }
