from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place


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
