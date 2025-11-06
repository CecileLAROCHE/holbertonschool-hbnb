from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # USERS
    def create_user(self, user_data, password=None):
        """
        Crée un utilisateur en hashant le mot de passe et en gérant le cas d'un admin.
        Évite les doublons sur l'email.
        """
        # Vérifie si l'utilisateur existe déjà
        existing_user = self.get_user_by_email(user_data["email"])
        if existing_user:
            print(f"⚠️ Utilisateur déjà existant : {existing_user.email}")
            return existing_user  # retourne l'utilisateur existant

        # Crée un nouvel utilisateur
        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"]
        )

        # Hash du mot de passe si fourni
        if password:
            user.hash_password(password)
        else:
            raise ValueError("Password is required to create a user")  # optionnel mais recommandé

        # Définir le statut admin si présent dans user_data
        user.is_admin = user_data.get("is_admin", False)

        # Sauvegarde dans la base via le repository
        self.user_repo.add(user)

        print(f"✅ Utilisateur créé : {user.email} (Admin: {user.is_admin})")
        return user

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

    def get_all_admins():
        """Return all users with is_admin=True"""
        from app.models.user import User
        return User.query.filter_by(is_admin=True).all()

    # AMENITIES

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)

    # PLACES
    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)

    # REVIEWS
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
