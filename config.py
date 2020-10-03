import os

class Config:
    '''
    This is the parent configuration class

    '''
    SECRET_KEY = "dfghjxfghjertyui45679dfhj"
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://arthur:Lastman@localhost/pitch'
    #  email configurations
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD")
class ProdConfig(Config):
    '''
     production configuration class which is a child of config class
    '''
    
    SQLALCHEMY_DATABASE_URI =os.environ.get("DATABASE_URL")

class DevConfig(Config):
    '''
    Development configuration class, child of the class Config
    '''
    DEBUG = True
    


config_options = {
'development':DevConfig,
'production':ProdConfig
}