from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.base_model import BaseModel
from app.persistence.repository import InMemoryRepository

api = Namespace('amenities', description='Amenity operations')

# Repository en mémoire pour gérer les amenities
amenity_repo = InMemoryRepository()

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


class Amenity(BaseModel):
    def __init__(self, name):
        if not name:
            raise ValueError("name is required")
        if len(name) > 50:
            raise ValueError("name must be at most 50 characters")
        super().__init__()
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'deleted_at': self.deleted_at.isoformat()
            if self.deleted_at else None
        }


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = api.payload
        try:
            new_amenity = Amenity(**data)
            amenity_repo.add(new_amenity)
            return new_amenity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = amenity_repo.get_all()
        return [a.to_dict() for a in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = amenity_repo.get(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = api.payload
        amenity = amenity_repo.get(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        name = data.get("name")
        if not name or not isinstance(name, str) or name.strip() == "":
            return {'error': 'Invalid name: must be a non-empty string'}, 400
        if len(name) > 50:
            return {'error': 'Invalid name: must not exceed 50 characters'
                    }, 400
        try:
            amenity.update(data)  # update() vient de BaseModel
            return amenity.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
