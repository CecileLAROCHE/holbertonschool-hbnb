import os


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = SECRET_KEY
    DEBUG = False


class DevelopmentConfig(Config):
    """Configuration pour le développement."""
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'development.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Dictionnaire des configurations disponibles
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
}
