from flask import Flask 
from flask_bootstrap import Bootstrap 
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail



login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'


bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()


def create_app(config_name):

    app = Flask(__name__)

    #creating the app configurations
    app.config.from_object(config_options[config_name])

    #Initializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)




    return app