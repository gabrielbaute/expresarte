from datetime import datetime
from typing import List, Optional

from flask import current_app
from app.database.controllers.db_controller import DatabaseController
from app.database.models import Calificacion, Usuario, CatedraAcademica


class CalificacionController(DatabaseController):
    """Controlador para gestión de calificaciones académicas"""

    def registrar_nota(
        self,
        alumno: Usuario,
        catedra: CatedraAcademica,
        nota: float,
        observaciones: Optional[str] = None
    ) -> Optional[Calificacion]:
        """Registra la nota final de un alumno en una cátedra específica"""
        if not alumno or not alumno.is_student():
            current_app.logger.warning("Usuario inválido o no es estudiante")
            return None

        if not catedra:
            current_app.logger.warning("Cátedra académica no especificada")
            return None

        existente = Calificacion.query.filter_by(
            alumno_id=alumno.id,
            catedra_academica_id=catedra.id
        ).first()

        if existente:
            current_app.logger.info("Ya existe una calificación para esta cátedra")
            return None

        nueva = Calificacion(
            alumno_id=alumno.id,
            catedra_academica_id=catedra.id,
            nota=nota,
            observaciones=observaciones or "",
            fecha=datetime.utcnow()
        )

        self.session.add(nueva)
        return nueva if self._commit_or_rollback() is True else None

    def editar_nota(
        self,
        calificacion_id: int,
        nueva_nota: float,
        nuevas_observaciones: Optional[str] = None
    ) -> bool:
        """Edita una calificación existente"""
        calificacion = Calificacion.query.get(calificacion_id)
        if not calificacion:
            return False
        calificacion.nota = nueva_nota
        if nuevas_observaciones is not None:
            calificacion.observaciones = nuevas_observaciones
        calificacion.fecha = datetime.utcnow()
        return self._commit_or_rollback() is True

    def eliminar_calificacion(self, calificacion_id: int) -> bool:
        """Elimina una calificación"""
        calificacion = Calificacion.query.get(calificacion_id)
        if not calificacion:
            return False
        self.session.delete(calificacion)
        return self._commit_or_rollback() is True

    def listar_por_alumno(self, alumno: Usuario) -> List[Calificacion]:
        """Devuelve el historial de calificaciones de un alumno"""
        return Calificacion.query.filter_by(alumno_id=alumno.id).order_by(Calificacion.fecha.desc()).all()

    def listar_por_catedra(self, catedra: CatedraAcademica) -> List[Calificacion]:
        """Devuelve todas las calificaciones asociadas a una cátedra"""
        return Calificacion.query.filter_by(catedra_academica_id=catedra.id).order_by(Calificacion.nota.desc()).all()

    def obtener_calificacion(self, alumno: Usuario, catedra: CatedraAcademica) -> Optional[Calificacion]:
        """Obtiene la calificación específica de un alumno en una cátedra"""
        return Calificacion.query.filter_by(
            alumno_id=alumno.id,
            catedra_academica_id=catedra.id
        ).first()
