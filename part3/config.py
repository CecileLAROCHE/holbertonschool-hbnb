import os


class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True


# Dictionnaire des configurations disponibles
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
