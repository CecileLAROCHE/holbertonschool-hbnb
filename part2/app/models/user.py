from app.models.base_model import BaseModel
import re


class User(BaseModel):
    """
    Represents a user in the HBnB application.

    Inherits from BaseModel and includes personal information,
    authentication credentials.
    """
    def __init__(self, first_name, last_name, email):
        """
    Represents a user in the HBnB application.

    Inherits from BaseModel and includes personal information,
    authentication credentials.
    """
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

    @staticmethod
    def _validate_email(email):
        """
        Validate the user's email format using a regular expression.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email is valid, False otherwise.
        """
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(pattern, email))
