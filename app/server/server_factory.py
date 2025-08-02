from flask import Flask
from datetime import datetime

from app.config import Config, create_initial_super_admin
from app.server.routes import register_blueprints
from app.server.server_extensions import init_login_manager, init_migrate, init_csrf
from app.database import db, init_db

def create_app():
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    
    app.config.from_object(Config)

    init_db(app)
    init_migrate(app, db)
    init_csrf(app)
    init_login_manager(app)
    register_blueprints(app)

    with app.app_context():
        db.create_all()
        create_initial_super_admin()
        if app.config.get("DEBUG", False):
            from app.seeds.academico_seed import generar_seed_academico
            generar_seed_academico()

    @app.context_processor
    def inject_app_name():
        return {
            "app_name": app.config["APP_NAME"],
            "app_version": app.config["APP_VERSION"],
            "server_language": app.config["LANGUAGE"],
            "now": datetime.now() 
            }

    return app