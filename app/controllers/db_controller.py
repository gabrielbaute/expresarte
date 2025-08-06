"""Controlador de base de datos"""
from typing import Any, Type
from pydantic import BaseModel
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from typing import Union

from app.errors.exceptions import NotFoundError

class DatabaseController:
    def __init__(self, db: SQLAlchemy):
        self.db = db
        self.session = self.db.session

    def _commit_or_rollback(self) -> Union[bool, str]:
        """Intenta hacer commit de la sesión actual.
        Si falla, hace rollback y devuelve el error.
        """
        try:
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            current_app.logger.error(f"[COMMIT ERROR] {e}")
            return str(e)

    def _to_response(self, instance: Any, schema: Type[BaseModel]) -> BaseModel:
        """
        Convierte instancia de ORM o dict en un schema de respuesta.
        """
        if not instance:
            raise NotFoundError("No se encontró el recurso")
        
        if isinstance(instance, dict):
            return schema(**instance)
        
        if isinstance(instance.__class__, DeclarativeMeta):
            return schema.model_validate(instance)

        raise TypeError(f"Tipo no soportado: {type(instance)}")

    def _bulk_to_response(self, instances: list[Any], schema: Type[BaseModel]) -> list[BaseModel]:
        """Convierte múltiples instancias ORM o dicts en schemas Pydantic"""
        return [self._to_response(i, schema) for i in instances if i]

    def _get_or_fail(self, model_class, object_id: int):
        """Obtiene un objeto por su ID o lanza NotFoundError si no existe."""
        obj = self.session.get(model_class, object_id)
        if obj is None:
            raise NotFoundError(f"{model_class.__name__} con ID {object_id} no encontrado.")
        return obj
