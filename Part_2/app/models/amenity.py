from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name, **kwargs):
        if not name:
            raise ValueError("name is required")
        if len(name) > 50:
            raise ValueError("name must be at most 50 characters")
        super().__init__(**kwargs)
        self.name = name
