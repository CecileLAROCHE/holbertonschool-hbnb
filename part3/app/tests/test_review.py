import unittest
from app.models.review import Review
from app.models.user import User
from app.models.place import Place
from app.models.basemodel import BaseModel


class TestReviewModel(unittest.TestCase):
    """Tests unitaires pour la classe Review"""

    def setUp(self):
        # Crée des instances valides pour les tests
        self.user = User(first_name="John",
                         last_name="Doe",
                         email="john@example.com",
                         password="secret123"
        )
        self.place = Place(title="Villa",
                           city_id="123",
                           user_id=self.user.id)
        # Réinitialiser les emails avant chaque test
        User.emails = set()

    def test_review_creation_valid(self):
        review = Review(text="Super endroit !", rating=5, place=self.place, user=self.user)
        self.assertEqual(review.text, "Super endroit !")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.place, self.place)
        self.assertEqual(review.user, self.user)

        expected_dict = {
            'id': review.id,
            'text': "Super endroit !",
            'rating': 5,
            'place_id': self.place.id,
            'user_id': self.user.id
        }
        self.assertEqual(review.to_dict(), expected_dict)

    def test_review_text_empty(self):
        with self.assertRaises(ValueError) as context:
            Review(text="", rating=5, place=self.place, user=self.user)
        self.assertEqual(str(context.exception), "Text cannot be empty")

    def test_review_text_type(self):
        with self.assertRaises(TypeError) as context:
            Review(text=123, rating=5, place=self.place, user=self.user)
        self.assertEqual(str(context.exception), "Text must be a string")

    def test_review_rating_type(self):
        with self.assertRaises(TypeError) as context:
            Review(text="Très bien", rating="5", place=self.place, user=self.user)
        self.assertEqual(str(context.exception), "Rating must be an integer")

    def test_review_rating_out_of_range(self):
        with self.assertRaises(ValueError) as context:
            Review(text="Pas terrible", rating=7, place=self.place, user=self.user)
        self.assertIn("Rating must be between", str(context.exception))

    def test_review_place_type(self):
        with self.assertRaises(TypeError) as context:
            Review(text="OK", rating=4, place="not_a_place", user=self.user)
        self.assertEqual(str(context.exception), "Place must be a place instance")

    def test_review_user_type(self):
        with self.assertRaises(TypeError) as context:
            Review(text="OK", rating=4, place=self.place, user="not_a_user")
        self.assertEqual(str(context.exception), "User must be a user instance")

    def test_review_update(self):
        review = Review(text="Bien", rating=4, place=self.place, user=self.user)
        review.text = "Excellent"
        review.rating = 5
        self.assertEqual(review.text, "Excellent")
        self.assertEqual(review.rating, 5)


if __name__ == "__main__":
    unittest.main()
