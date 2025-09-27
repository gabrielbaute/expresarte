from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask

from app.database import db
from app.database.models import Usuario

login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def init_login_manager(app: Flask):
    """Función que inicializa la extensión LoginManager.
    
    Args:
        app (Flask): Instancia de la aplicación Flask.
    
    Returns:
        LoginManager: Instancia de la extensión LoginManager.
    """
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, inicie sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        """Función que carga un usuario por su ID.
        
        Args:
            user_id (int): ID del usuario.
        
        Returns:
            Usuario: Instancia del usuario.
        """
        return db.session.get(Usuario, int(user_id))

    return login_manager

def init_migrate(app: Flask, db: SQLAlchemy):
    """Función que inicializa la extensión Migrate.
    
    Args:
        app (Flask): Instancia de la aplicación Flask.
        db (SQLAlchemy): Instancia de la base de datos SQLAlchemy.
    """
    migrate.init_app(app, db)

def init_csrf(app: Flask):
    """Función que inicializa la extensión CSRFProtect.
    
    Args:
        app (Flask): Instancia de la aplicación Flask.
    """
    app.config['WTF_CSRF_ENABLED'] = True
    csrf.init_app(app)