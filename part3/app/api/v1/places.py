from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import get_facade

facade = get_facade()

api = Namespace('places', description='Place operations')

# Models
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('Review', {
    'rating': fields.Integer(required=True, description='Rating from 1 to 5'),
    'comment': fields.String(description='Comment for the review')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True,
                             description="List of amenities ID's")
})


# ---------- ROUTE : /places ----------
@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        current_user_id = get_jwt_identity()
        place_data = api.payload
        place_data['owner_id'] = current_user_id
        place_data.pop('owner', None)

        try:
            new_place, created = facade.create_place(place_data)
            if not created:
                return {'message': 'Place already exists'}, 400
            return new_place.to_dict(), 201
        except KeyError:
            return {'error': 'Invalid input data'}, 400
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places, ok = facade.get_all_places()
        if not ok or not places:
            return {'message': 'No places found'}, 200
        return [p.to_dict() for p in places], 200


# ---------- ROUTE : /places/<place_id> ----------
@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place, ok = facade.get_place(place_id)
        if not ok:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        place, ok = facade.get_place(place_id)
        if not ok:
            return {'error': 'Place not found'}, 404

        if place.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        try:
            updated_place, ok = facade.update_place(place_id, api.payload)
            if not ok:
                return {'error': 'Place not found'}, 404
            return updated_place.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.response(200, 'Place successfully deleted')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, place_id):
        """Delete a place (only the owner or admin can do it)"""
        current_user_id = get_jwt_identity()
        user, ok = facade.get_user(current_user_id)
        if not ok:
            return {'error': 'User not found'}, 404

        place, ok = facade.get_place(place_id)
        if not ok:
            return {'error': 'Place not found'}, 404

        # Vérifie si l'utilisateur est le propriétaire ou un admin
        if place.owner_id != user.id and not user.is_admin:
            return {'error': 'Unauthorized action'}, 403

        deleted_place, ok = facade.delete_place(place_id, user.id)
        if not ok:
            return {'error': 'Could not delete place'}, 400

        return {'message': 'Place successfully deleted'}, 200


# ---------- ROUTE : /places/<place_id>/amenities ----------
@api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @api.expect([amenity_model])
    @api.response(200, 'Amenities added successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def post(self, place_id):
        """Add amenities to a place"""
        amenities_data = api.payload
        if not amenities_data or len(amenities_data) == 0:
            return {'error': 'Invalid input data'}, 400

        place, ok = facade.get_place(place_id)
        if not ok:
            return {'error': 'Place not found'}, 404

        for amenity_item in amenities_data:
            amenity_id = amenity_item.get('id')
            amenity, found = facade.get_amenity(amenity_id)
            if not found:
                return {'error': f"Amenity {amenity_id} not found"}, 400
            place.add_amenity(amenity)

        return {'message': 'Amenities added successfully'}, 200

    @api.response(200, 'Amenities retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve all amenities of a place"""
        place, ok = facade.get_place(place_id)
        if not ok:
            return {'error': 'Place not found'}, 404
        return [a.to_dict() for a in place.amenities], 200


# ---------- ROUTE : /places/<place_id>/reviews ----------
@api.route('/<place_id>/reviews/')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place (public)"""
        place, ok = facade.get_place(place_id)
        if not ok:
            return {'error': 'Place not found'}, 404
        return [review.to_dict() for review in place.reviews], 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self, place_id):
        """Create a review for a place"""
        current_user = get_jwt_identity()
        place, ok = facade.get_place(place_id)
        if not ok:
            return {'error': 'Place not found'}, 404

        if place.owner_id == current_user:
            return {'error': 'You cannot review your own place'}, 400

        for r in place.reviews:
            if r.user_id == current_user:
                return {'error': 'You have already reviewed this place'}, 400

        review_data = api.payload
        review_data['user_id'] = current_user
        review_data['place_id'] = place_id

        new_review, created = facade.create_review(review_data)
        if not created:
            return {'error': 'Could not create review'}, 400

        return new_review.to_dict(), 201
