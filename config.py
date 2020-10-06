import os

class Config:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    # UPLOADED_PHOTOS_DEST ='app/static/photos'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USE_SSL = True
    SECRET_KEY ='QWERTY'
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://arthur_earl:arthur@localhost/pitch'
    DEBUG = True

class TestsConfig(Config):
    """
    Testing config child class
    Args:
        Config: The parent config class with general config classes
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://arthur_earl:arthur@localhost/pitch'
    DEBUG = True
    



config_options = {
    'development':DevConfig,
    'tests':TestsConfig,
    'production':ProdConfig
    
}