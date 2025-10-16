from app.models.base_model import BaseModel
from time import sleep


# Création d’un objet
obj = BaseModel()
print(obj.id)
print(obj.created_at, obj.updated_at, obj.deleted_at)

# Test du save()
sleep(1)
obj.save()
print(obj.updated_at)  # doit être plus récent

# Test de update()
sleep(1)
obj.name = "Initial Name"
obj.update({"name": "Updated Name"})
print("Nom mis à jour:", obj.name)
print("Après update(), updated_at:", obj.updated_at)  # encore plus récent

# Test du delete()
obj.delete()
print(obj.deleted_at)  # doit être une date
