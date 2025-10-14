from app.models.base_model import BaseModel
import re
import hashlib
import os


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False,
                 password=None):
        super().__init__()
        if not first_name or len(first_name) > 50:
            raise ValueError("first_name must be 1-50 characters")
        if not last_name or len(last_name) > 50:
            raise ValueError("last_name must be 1-50 characters")
        if not User._validate_email(email):
            raise ValueError("Invalid email format")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self._salt = os.urandom(16)
        self._password = self._hash_password(password or "", self._salt)

    @staticmethod
    def _validate_email(email):
        """Check if the user's email is in a valid format"""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(pattern, email))

    def _hash_password(self, password, salt):
        """Hash the password using SHA256 and the provided salt"""
        return hashlib.sha256(password.encode() + salt).digest()

    def verify_password(self, password):
        """Verify if the given password matches the stored hash"""
        return self._hash_password(password, self._salt) == self._password