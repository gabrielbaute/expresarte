from flask import Flask
from flask_migrate import Migrate
from datetime import datetime

from app.config import Config
from app.database import db, init_db

def create_app():
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    
    app.config.from_object(Config)

    init_db(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    @app.context_processor
    def inject_app_name():
        return {
            "app_name": app.config["APP_NAME"],
            "app_version": app.config["APP_VERSION"],
            "server_language": app.config["LANGUAGE"],
            "now": datetime.now() 
            }

    return app