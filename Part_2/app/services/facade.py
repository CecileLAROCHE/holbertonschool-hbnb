from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """
    Facade class providing a simplified interface to interact with
    the underlying repositories and domain models (User, Place,
    Amenity, Review).

    It handles CRUD operations and validation logic for each entity.
    """
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # --- Users ---
    def create_user(self, user_data):
        """
        Create a new User instance and store it in the repository.

        Args:
            user_data (dict): Dictionary containing user attributes.

        Returns:
            User: The newly created user object.
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieve a user by their unique ID.

        Args:
            user_id (str): The UUID of the user.

        Returns:
            User | None: The user if found, otherwise None.
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieve a user by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            User | None: The user if found, otherwise None.
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """
        Return a list of all users.

        Returns:
            list[User]: A list of all stored users.
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, update_data):
        """
        Update user attributes with new data.

        Args:
            user_id (str): The UUID of the user.
            update_data (dict): Dictionary of updated attributes.

        Returns:
            User | None: The updated user if found, otherwise None.
        """
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        self.user_repo._storage[user.id] = user
        return user

    # --- Amenities ---
    def create_amenity(self, data):
        """
        Create and store a new Amenity.

        Args:
            data (dict): Dictionary containing amenity attributes.

        Returns:
            Amenity: The newly created amenity.
        """
        amenity = Amenity(**data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by ID.

        Args:
            amenity_id (str): The UUID of the amenity.

        Returns:
            Amenity | None: The amenity if found, otherwise None.
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Return all amenities.

        Returns:
            list[Amenity]: A list of all amenities.
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        """
        Update an existing amenity’s attributes.

        Args:
            amenity_id (str): The UUID of the amenity.
            data (dict): Dictionary containing updated attributes.

        Returns:
            Amenity | None: The updated amenity if found, otherwise None.
        """
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(data)
        return amenity

    # --- Places ---
    def create_place(self, place_data):
        """
        Validate and create a new Place.

        Args:
            place_data (dict): Dictionary containing place attributes.

        Raises:
            ValueError: If price is invalid or negative.

        Returns:
            Place: The newly created place.
        """
        price = place_data.get('price', 0)
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValueError("price must be a number")
        if price < 0:
            raise ValueError("Price must be positive")
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """
        Retrieve a place by ID, including its owner and amenities.

        Args:
            place_id (str): The UUID of the place.

        Returns:
            Place | None: The place object if found, otherwise None.
        """
        place = self.place_repo.get(place_id)
        place = self.place_repo.get(place_id)
        if not place:
            return None
        owner = self.user_repo.get(place.owner_id)
        place.owner = owner
        if hasattr(place, 'amenities_ids'):
            amenities = [self.amenity_repo.get(a_id) for a_id
                         in place.amenities_ids]
            place.amenities = [a for a in amenities if a]
        return place

    def get_all_places(self):
        """
        Retrieve all places, attaching their owners and amenities.

        Returns:
            list[Place]: A list of all places.
        """
        places = self.place_repo.get_all()
        for place in places:
            owner = self.user_repo.get(place.owner_id)
            place.owner = owner
            if hasattr(place, 'amenities_ids'):
                amenities = [self.amenity_repo.get(a_id) for a_id
                             in place.amenities_ids]
                place.amenities = [a for a in amenities if a]
        return places

    def update_place(self, place_id, place_data):
        """
        Update existing place attributes.

        Args:
            place_id (str): The UUID of the place.
            place_data (dict): Dictionary containing updated attributes.

        Returns:
            Place | None: The updated place if found, otherwise None.
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None
        for key, value in place_data.items():
            if hasattr(place, key):
                setattr(place, key, value)
        self.place_repo._storage[place.id] = place
        return place

    # --- Review ---
    def create_review(self, review_data):
        """
        Validate review input and create a new Review object.

        Args:
            review_data (dict): Dictionary containing review details.

        Raises:
            ValueError: If user/place does not exist
            or invalid data is provided.

        Returns:
            Review: The created review instance.
        """
        user = self.get_user(review_data['user_id'])
        place = self.get_place(review_data['place_id'])
        text = review_data.get('text')
        rating = review_data.get('rating')
        if not user or not place:
            raise ValueError("User or Place does not exist")
        if not text or not isinstance(text, str):
            raise ValueError("Review text must be a non-empty string")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=user.id,
            place_id=place.id,
        )
        place.add_review(review)
        return review

    def get_review(self, review_id):
        """
        Retrieve a review by its ID by searching through all places.

        Args:
            review_id (str): The UUID of the review.

        Returns:
            Review | None: The review if found, otherwise None.
        """
        for place in self.get_all_places():
            for review in place.reviews:
                if review.id == review_id:
                    return review
        return None

    def get_all_reviews(self):
        """
        Return all reviews across all places.

        Returns:
            list[Review]: A list of all reviews.
        """
        reviews = []
        for place in self.get_all_places():
            reviews.extend(place.reviews)
        return reviews

    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews associated with a specific place.

        Args:
            place_id (str): The UUID of the place.

        Returns:
            list[Review] | None: A list of reviews or None if place not found.
        """
        place = self.get_place(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        """
        Update review text or rating if it exists.

        Args:
            review_id (str): The UUID of the review.
            review_data (dict): Dictionary of updated review fields.

        Returns:
            Review | None: The updated review if found, otherwise None.
        """
        review = self.get_review(review_id)
        if not review:
            return None
        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']
        return review
