from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


# Création du moteur SQLAlchemy
# 🔹 utilise un fichier SQLite local nommé "hbnb.db"
engine = create_engine("sqlite:///hbnb.db", echo=False)

# Classe de base pour tous les modèles ORM
Base = declarative_base()


def init_db():
    """Crée toutes les tables définies par les modèles."""
    import app.models.user  # importe tous les modèles ici
    import app.models.place
    import app.models.review
    import app.models.amenity
    Base.metadata.create_all(engine)
