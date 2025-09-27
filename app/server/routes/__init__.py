"""Registro de los blueprints"""
from flask import Flask
from app.server.routes.main_routes import main_bp
from app.server.routes.auth_routes import auth_bp
from app.server.routes.admin_routes import admin_bp
from app.server.routes.teacher_routes import teacher_bp

def register_blueprints(app: Flask) -> None:
    """Registro de los blueprints
    
    Args:
        app (Flask): instancia de la app Flask
    """
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(teacher_bp)