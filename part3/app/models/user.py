from .basemodel import BaseModel
import re


class User(BaseModel):
    # Ensemble pour stocker tous les emails existants et éviter les doublons
    emails = set()

    def __init__(self,
                 first_name,
                 last_name,
                 email,
                 is_admin=False,
                 password=None):
        # Appel du constructeur parent (BaseModel)
        super().__init__()
        # Initialisation des attributs de l'utilisateur
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []   # Liste des lieux associés à l'utilisateur
        self.reviews = []  # Liste des avis associés à l'utilisateur
        # Si un mot de passe est fourni, on le hache
        if password:
            self.hash_password(password)
        else:
            self.password = None

    def hash_password(self, password):
        """Hache le mot de passe avant de le stocker."""
        from app import bcrypt
        if password:
            self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Vérifie si le mot de passe fourni correspond au hash stocké."""
        from app import bcrypt
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)

    # ---------- Gestion du prénom ----------
    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        # Vérifie que la valeur est une chaîne de caractères
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        # Vérifie la longueur maximale autorisée (via BaseModel)
        super().is_max_length('First name', value, 50)
        self.__first_name = value

    # ---------- Gestion du nom ----------
    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        # Vérifie que la valeur est une chaîne de caractères
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        # Vérifie la longueur maximale autorisée
        super().is_max_length('Last name', value, 50)
        self.__last_name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        # Vérifie que la valeur est une chaîne de caractères
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        # Vérifie le format de l'email avec une expression régulière
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        # Vérifie que l'email n'existe pas déjà
        if value in User.emails:
            raise ValueError("Email already exists")
        # Si l'instance a déjà un email, on le retire de la liste globale
        if hasattr(self, "_User__email"):
            User.emails.discard(self.__email)
        # On assigne le nouvel email et on l'ajoute à la liste des emails
        # existants
        self.__email = value
        User.emails.add(value)

    # ---------- Gestion du statut admin ----------
    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        # Vérifie que la valeur est un booléen
        if not isinstance(value, bool):
            raise TypeError("Is Admin must be a boolean")
        self.__is_admin = value

    # ---------- Gestion des lieux associés ----------
    def add_place(self, place):
        """Ajoute un lieu à la liste des places de l'utilisateur."""
        self.places.append(place)

    # ---------- Gestion des avis associés ----------
    def add_review(self, review):
        """Ajoute un avis à la liste des reviews de l'utilisateur."""
        self.reviews.append(review)

    def delete_review(self, review):
        """Supprime un avis de la liste des reviews de l'utilisateur."""
        self.reviews.remove(review)

    # ---------- Conversion en dictionnaire ----------
    def to_dict(self):
        """Retourne une représentation dictionnaire de l'utilisateur
        (sans mot de passe)."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
