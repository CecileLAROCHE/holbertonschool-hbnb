# app/models/base_model.py

# Importations nécessaires (uuid, datetime, etc.)

class BaseModel:
    """Classe de base pour tous les modèles HBnB."""

    # Méthode d'initialisation
    def __init__(...):
        # création d'un id unique
        # enregistrement des dates

    # Méthode pour convertir en dictionnaire
    def to_dict(...):
        # retourne les attributs de l'objet sous forme de dict

    # Méthode de mise à jour
    def update(...):
        # met à jour les champs modifiables

    # Méthode d'affichage optionnelle (__str__ ou __repr__)