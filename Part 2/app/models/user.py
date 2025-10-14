from app.models.base_model import BaseModel
import re
import hashlib
import os


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password,
                 administrator=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self._salt = os.urandom(16)
        self._password = self._hash_password(password, self._salt)
        self.administrator = administrator

    def verify_email(self):
        """Check if the user's email is in a valid format"""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if re.match(pattern, self.email):
            return True
        else:
            return False

    def _hash_password(self, password, salt):
        """Hash the password using SHA256 and the provided salt"""
        return hashlib.sha256(password.encode() + salt).digest()

    def verify_password(self, password):
        """Verify if the given password matches the stored hash"""
        new_hash = self._hash_password(password, self._salt)
        return new_hash == self._password
