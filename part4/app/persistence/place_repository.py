from app.persistence.repository import SQLAlchemyRepository
from app.models.place import Place


class PlaceRepository(SQLAlchemyRepository[Place]):
    def __init__(self):
        super().__init__(Place)

    def get_by_owner(self, owner_id):
        return self.session.query(self.model).filter_by(owner_id=owner_id).all()
