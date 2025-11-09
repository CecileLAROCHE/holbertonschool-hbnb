from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository
from app import db


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # USERS
    def create_user(self, user_data, password=None):
        """
        Crée un utilisateur en hashant le mot de passe et
        en gérant le cas d'un admin. Evite les doublons sur l'email.
        """
        # Vérifie si l'utilisateur existe déjà
        existing_user = self.get_user_by_email(user_data["email"])
        if existing_user:
            print(f"⚠️ Utilisateur déjà existant : {existing_user.email}")
            return existing_user, False
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
            raise ValueError("Password is required to create a user")

        # Définir le statut admin si présent dans user_data
        user.is_admin = user_data.get("is_admin", False)

        # Sauvegarde dans la base via le repository
        self.user_repo.add(user)

        print(f"✅ Utilisateur créé : {user.email} (Admin: {user.is_admin})")
        return user, True  # <-- ⚠️ ICI aussi on renvoie un tuple (user, True)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('_email', email)

    def get_user(self, user_id):
        """Récupère un utilisateur par son ID"""
        user = self.user_repo.get(user_id)
        if not user:
            return None, False
        return user, True

    def get_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

    def get_all_admins(self):
        """Return all users with is_admin=True"""
        from app.models.user import User
        return [u for u in User.query.all() if getattr(u, "is_admin", False)]

    # AMENITIES

    def create_amenity(self, amenity_data):
        """Crée une amenity si elle n'existe pas déjà (nom unique)"""
        name = amenity_data.get("name")
        if not name:
            return {"error": "Name is required"}, False

        # Vérifie si une amenity avec le même nom existe déjà
        existing = self.amenity_repo.get_by_attribute("name", name)
        if existing:
            return {"error": f"Amenity '{existing.name}' already exists",
                    "id": existing.id}, False

        try:
            amenity = Amenity(**amenity_data)
            self.amenity_repo.add(amenity)
            return amenity, True
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, False

    def get_all_amenities(self):
        """Récupère toutes les amenities"""
        amenities = self.amenity_repo.get_all()
        return amenities if amenities else []

    def get_amenity(self, amenity_id):
        """Récupère une amenity par son ID"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None, False
        return amenity, True

    def get_amenity_by_name(self, name):
        """Retourne une amenity par son nom, ou None si elle n'existe pas"""
        if not name:
            return None
        return self.amenity_repo.get_by_attribute("name", name)

    def update_amenity(self, amenity_id, amenity_data):
        """Met à jour une amenity existante"""
        amenity = self.amenity_repo.update(amenity_id, amenity_data)
        if not amenity:
            return None, False
        return amenity, True

    def delete_amenity(self, amenity_id):
        """Supprime une amenity"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None, False
        self.amenity_repo.delete(amenity_id)
        return amenity, True

    # PLACES
    def create_place(self, place_data):
        """Crée une nouvelle place si elle n'existe pas déjà"""
        # Vérifie si une place identique existe déjà
        existing_place = next(
            (p for p in self.place_repo.get_all()
                if p.title == place_data.get('title')
                and p.owner_id == place_data.get('owner_id')),
            None
        )
        if existing_place:
            return existing_place, False

        # Crée l'objet Place à partir du dict
        place = Place(**place_data)
        # Ajoute via le repository
        self.place_repo.add(place)
        return place, True

    def get_place(self, place_id):
        """Récupère une place par son ID"""
        place = self.place_repo.get_by_id(place_id)
        if not place:
            return None, False
        return place, True

    def get_all_places(self):
        """Récupère toutes les places"""
        places = self.place_repo.get_all()
        return places, True if places else ([], False)

    def update_place(self, place_id, place_data):
        """Met à jour une place"""
        updated_place = self.place_repo.update(place_id, place_data)
        if not updated_place:
            return None, False
        return updated_place, True

    def delete_place(self, place_id, user_id):
        """Supprime une place si l'utilisateur est le propriétaire"""
        place = self.place_repo.get_by_id(place_id)
        if not place:
            return None, False  # place introuvable

        if place.owner_id != user_id:
            return None, False  # action non autorisée

        self.place_repo.delete(place_id)
        return place, True

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
