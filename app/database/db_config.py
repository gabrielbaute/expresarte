from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app: Flask):
    """Inicializa la base de datos
    
    Args:
        app (Flask): Instancia de la aplicación Flask
    """
    db.init_app(app)