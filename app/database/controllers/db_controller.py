"""Controlador de base de datos"""
from app.database.db_config import db

class DatabaseController:
    def __init__(self):
        self.session = db.session

    @staticmethod
    def _commit_or_rollback():
        """Helper para manejar commit/rollback."""
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return str(e)