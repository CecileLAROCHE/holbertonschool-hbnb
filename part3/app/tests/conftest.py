import pytest
from app.models.user import User


@pytest.fixture(autouse=True)
def reset_user_emails():
    User.emails = set()
