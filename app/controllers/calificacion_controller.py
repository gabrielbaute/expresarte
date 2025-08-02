from datetime import datetime
from typing import List, Optional

from app.controllers.db_controller import DatabaseController
from app.database.models import Calificacion
from app.schemas.calificaciones import (
    CalificacionCreate,
    CalificacionUpdate,
    CalificacionResponse
)
from app.errors.exceptions import NotFoundError, PermissionDeniedError

class CalificacionController(DatabaseController):
    """Controlador para gestión de calificaciones académicas"""
    def __init__(self, db, current_user=None):
        super().__init__(db)
        self.current_user = current_user

    def registrar_calificacion(self, data: CalificacionCreate) -> CalificacionResponse:
        """Registra la nota final de un alumno en una cátedra específica"""
        existente = self.session.query(Calificacion).filter_by(
            estudiante_id=data.estudiante_id,
            catedra_academica_id=data.catedra_academica_id
        ).first()

        if existente:
            raise PermissionDeniedError("Ya existe una calificación registrada para esta cátedra")

        nueva = Calificacion(
            estudiante_id=data.estudiante_id,
            catedra_academica_id=data.catedra_academica_id,
            periodo_id=data.periodo_id,
            calificacion=data.calificacion,
            observaciones=data.observaciones or "",
            fecha=datetime.utcnow()
        )

        self.session.add(nueva)
        self._commit_or_rollback()
        return self._to_response(nueva, CalificacionResponse)

    def editar_calificacion(self, calificacion_id: int, data: CalificacionUpdate) -> CalificacionResponse:
        """Edita una calificación existente"""
        calificacion = self._get_or_fail(Calificacion, calificacion_id)

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(calificacion, field, value)

        calificacion.fecha = datetime.utcnow()

        self._commit_or_rollback()
        return self._to_response(calificacion, CalificacionResponse)

    def eliminar_calificacion(self, calificacion_id: int) -> bool:
        """Elimina una calificación"""
        calificacion = self._get_or_fail(Calificacion, calificacion_id)
        self.session.delete(calificacion)
        return self._commit_or_rollback() is True

    def listar_por_estudiante(self, estudiante_id: int) -> List[CalificacionResponse]:
        """Devuelve el historial de calificaciones de un estudiante"""
        calificaciones = self.session.query(Calificacion).filter_by(
            estudiante_id=estudiante_id
        ).order_by(Calificacion.fecha.desc()).all()

        return self._bulk_to_response(calificaciones, CalificacionResponse)

    def listar_por_catedra(self, catedra_id: int) -> List[CalificacionResponse]:
        """Devuelve todas las calificaciones asociadas a una cátedra"""
        calificaciones = self.session.query(Calificacion).filter_by(
            catedra_academica_id=catedra_id
        ).order_by(Calificacion.calificacion.desc()).all()

        return self._bulk_to_response(calificaciones, CalificacionResponse)

    def obtener_calificacion(self, estudiante_id: int, catedra_id: int) -> Optional[CalificacionResponse]:
        """Obtiene la calificación específica de un alumno en una cátedra"""
        resultado = self.session.query(Calificacion).filter_by(
            estudiante_id=estudiante_id,
            catedra_academica_id=catedra_id
        ).first()

        return self._to_response(resultado, CalificacionResponse) if resultado else None