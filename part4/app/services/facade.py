from typing import Optional

from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.amenity_repository import AmenityRepository
from app.persistence.review_repository import ReviewRepository

from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = AmenityRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()

    # USER
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id) -> Optional[User]:
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email) -> Optional[User]:
        return self.user_repo.get_user_by_email(email=email)

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)

    # AMENITY
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)

    # PLACE
    def create_place(self, place_data):
        print("in create place")
        user = self.user_repo.get(place_data['owner_id'])
        if not user:
            raise KeyError('Invalid input data')
        place_data['owner'] = user
        del place_data['owner_id']

        amenities = place_data.pop('amenities', None)
        place = Place(**place_data)
        if amenities:
            for amenity_id in amenities:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise KeyError(f'Invalid amenity id: {amenity_id}')
                place.amenities.append(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id) -> Place:
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)

    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError("Place not found")

        # Supprimer toutes les reviews liées avant de supprimer le lieu
        for review in list(place.reviews):
            self.delete_review(review.id)

        self.place_repo.delete(place_id)

    def get_places_by_user(self, user_id):
        # Si ta relation est 'owner_id' dans Place :
        return self.place_repo.get_by_owner(user_id)

    # REVIEWS
    def create_review(self, review_data):
        """Crée une nouvelle review."""
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise KeyError('Invalid input data')
        del review_data['user_id']
        review_data['user'] = user

        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise KeyError('Invalid input data')
        del review_data['place_id']
        review_data['place'] = place

        review = Review(**review_data)
        self.review_repo.add(review)
        # SQLAlchemy gère déjà review.user et review.place
        return review

    def get_review(self, review_id):
        """Récupère une review par son ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Récupère toutes les reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Récupère toutes les reviews d'un lieu."""
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError('Place not found')
        return place.reviews

    def update_review(self, review_id, review_data):
        """Met à jour une review existante."""
        self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """Supprime une review."""
        review = self.review_repo.get(review_id)
        if not review:
            raise KeyError('Review not found')
        self.review_repo.delete(review_id)
