from flask_restx import Namespace, Resource, fields
from app.services import facade

# Create a namespace for Place-related endpoints
api = Namespace('places', description='Place operations')

# Models amenity
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String,
    'name': fields.String
})
# Models owner
user_model = api.model('PlaceUser', {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String
})

# Model Place
place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String, required=True)
})


@api.route('/')
class PlaceList(Resource):
    """Resource for managing the collection of places."""

    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new place.

        Expects:
            JSON payload following the `place_model` schema.

        Returns:
            dict: The newly created place as a JSON object.
            int: HTTP 201 status code on success, 400 on invalid data.
        """
        data = api.payload
        try:
            new_place = facade.create_place(data)
            return new_place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve all existing places.

        Returns:
            list: A list of serialized place dictionaries.
            int: HTTP 200 status code.
        """
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    """Resource for managing individual places."""

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve details for a specific place by ID.

        Args:
            place_id (str): The UUID of the place to retrieve.

        Returns:
            dict: Place details if found.
            int: HTTP 200 on success, 404 if not found.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """
        Update an existing place by its ID.

        Args:
            place_id (str): The UUID of the place to update.

        Expects:
            JSON payload following the `place_model` schema.

        Returns:
            dict: The updated place as a JSON object.
            int: HTTP 200 on success, 404 if not found, 400 on invalid input.
        """
        data = api.payload
        try:
            updated_place = facade.update_place(place_id, data)
            if not updated_place:
                return {'error': 'Place not found'}, 404
            return updated_place.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
