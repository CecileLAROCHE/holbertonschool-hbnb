from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.services import get_facade
from app.api.v1.auth import is_admin

api = Namespace('amenities', description='Amenity operations')
facade = get_facade()

# Modèle Swagger pour les amenities
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data or already exists')
    @api.response(403, 'Forbidden — only admin users can create amenities')
    def post(self):
        """Create a new amenity (Admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload
        amenity, ok = facade.create_amenity(amenity_data)

        if not ok:
            # Amenity déjà existante, facade renvoie dict avec ID
            return amenity, 400

        return amenity.to_dict(), 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        if not amenities:
            return {'error': 'No amenities found'}, 404
        return [a.to_dict() for a in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity, ok = facade.get_amenity(amenity_id)
        if not ok:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Forbidden — only admin users can update amenities')
    def put(self, amenity_id):
        """Update an existing amenity (Admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload
        updated_amenity, ok = facade.update_amenity(amenity_id, amenity_data)
        if not ok:
            return {'error': 'Amenity not found'}, 404
        return updated_amenity.to_dict(), 200

    @jwt_required()
    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Forbidden — only admin users can delete amenities')
    def delete(self, amenity_id):
        """Delete an existing amenity (Admin only)"""
        if not is_admin():
            return {'error': 'Admin privileges required'}, 403

        deleted_amenity, ok = facade.delete_amenity(amenity_id)
        if not ok:
            return {'error': 'Amenity not found'}, 404
        return {'message': 'Amenity deleted successfully'}, 200
