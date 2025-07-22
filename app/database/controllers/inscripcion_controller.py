from datetime import datetime
from typing import List, Optional

from flask import current_app
from app.database.controllers.db_controller import DatabaseController
from app.database.models import Inscripcion, Usuario, CatedraAcademica


class InscripcionController(DatabaseController):
    """Controlador para gestionar inscripciones de alumnos a cátedras académicas"""

    def inscribir_alumno(self, alumno: Usuario, catedra: CatedraAcademica) -> Optional[Inscripcion]:
        """Inscribe a un alumno en una cátedra si cumple condiciones de rol y cupos"""
        if not alumno or not alumno.is_student():
            current_app.logger.warning("El usuario no es un alumno válido")
            return None

        if not catedra:
            current_app.logger.warning("Cátedra académica no especificada")
            return None

        cupo_actual = Inscripcion.query.filter_by(
            catedra_academica_id=catedra.id,
            estado="activo"
        ).count()

        if cupo_actual >= catedra.cupos:
            current_app.logger.info(f"No hay cupos disponibles en la cátedra {catedra.id}")
            return None

        existente = Inscripcion.query.filter_by(
            alumno_id=alumno.id,
            catedra_academica_id=catedra.id,
            estado="activo"
        ).first()

        if existente:
            current_app.logger.info(f"El alumno {alumno.email} ya está inscrito en la cátedra {catedra.id}")
            return None

        nueva = Inscripcion(
            alumno_id=alumno.id,
            catedra_academica_id=catedra.id,
            estado="activo"
        )

        self.session.add(nueva)
        return nueva if self._commit_or_rollback() is True else None

    def cambiar_estado(self, inscripcion_id: int, nuevo_estado: str) -> bool:
        """Actualiza el estado de una inscripción"""
        insc = Inscripcion.query.get(inscripcion_id)
        if not insc or nuevo_estado not in ["activo", "retirado", "aprobado"]:
            return False
        insc.estado = nuevo_estado
        return self._commit_or_rollback() is True

    def eliminar_inscripcion(self, inscripcion_id: int) -> bool:
        """Elimina la inscripción directamente (solo si no hay evaluaciones vinculadas, opcional)"""
        insc = Inscripcion.query.get(inscripcion_id)
        if not insc:
            return False
        self.session.delete(insc)
        return self._commit_or_rollback() is True

    def listar_por_alumno(self, alumno: Usuario) -> List[Inscripcion]:
        """Devuelve todas las inscripciones de un alumno"""
        return Inscripcion.query.filter_by(alumno_id=alumno.id).order_by(Inscripcion.fecha_inscripcion.desc()).all()

    def listar_por_catedra(self, catedra: CatedraAcademica) -> List[Inscripcion]:
        """Devuelve todas las inscripciones activas en una cátedra"""
        return Inscripcion.query.filter_by(catedra_academica_id=catedra.id).order_by(Inscripcion.fecha_inscripcion.desc()).all()

    def obtener_inscripcion(self, inscripcion_id: int) -> Optional[Inscripcion]:
        """Obtiene una inscripción específica"""
        return Inscripcion.query.get(inscripcion_id)
