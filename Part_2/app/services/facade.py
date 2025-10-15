from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # --- Users ---
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, update_data):
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
        amenity = Amenity(**data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(data)
        return amenity

    # --- Places ---
    def create_place(self, place_data):
        price = place_data.get('price', 0)
        latitude = place_data.get('latitude')
        longitude = place_data.get('longitude')
        if price < 0:
            raise ValueError("Price must be non-negative")
        if latitude is not None and (latitude < -90 or latitude > 90):
            raise ValueError("Latitude must be between -90 and 90")
        if longitude is not None and (longitude < -180 or longitude > 180):
            raise ValueError("Longitude must be between -180 and 180")
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
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
        place = self.place_repo.get(place_id)
        if not place:
            return None
        for key, value in place_data.items():
            if hasattr(place, key):
                if key == 'price' and value < 0:
                    raise ValueError("Price must be non-negative")
                if key == 'latitude' and (value < -90 or value > 90):
                    raise ValueError("Latitude must be between -90 and 90")
                if key == 'longitude' and (value < -180 or value > 180):
                    raise ValueError("Longitude must be between -180 and 180")
                setattr(place, key, value)
        self.place_repo._storage[place.id] = place
        return place

    # --- Review ---
    def create_review(self, review_data):
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
        for place in self.get_all_places():
            for review in place.reviews:
                if review.id == review_id:
                    return review
        return None

    def get_all_reviews(self):
        reviews = []
        for place in self.get_all_places():
            reviews.extend(place.reviews)
        return reviews

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']
        return review
