from flask import Flask
from .extensions import db, login_manager
from .config import Config
from .routes.main import main
from .routes.user import user
from .routes.forms import forms

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(forms)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    login_manager.login_message = ''

    with app.app_context():
        db.create_all()

    return app
