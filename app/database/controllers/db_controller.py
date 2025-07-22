"""Controlador de base de datos"""
from app.database.db_config import db

class DatabaseController:
    def __init__(self):
        self.session = db.session

    def _commit_or_rollback(self):
        try:
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"[COMMIT ERROR] {e}")
            return str(e)