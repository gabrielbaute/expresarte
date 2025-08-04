from typing import List
from app.controllers.db_controller import DatabaseController
from app.database.models import Inscripcion, CatedraAcademica
from app.schemas.inscripciones import InscripcionCreate, InscripcionUpdate, InscripcionResponse
from app.errors.exceptions import NotFoundError, PermissionDeniedError


class InscripcionController(DatabaseController):
    """Controlador para gestionar inscripciones de alumnos a cátedras académicas"""
    def __init__(self, db, current_user=None):
        super().__init__(db)
        self.current_user = current_user

    def inscribir_alumno(self, data: InscripcionCreate) -> InscripcionResponse:
        """Inscribe a un alumno en una cátedra si cumple condiciones de rol y cupos"""
        # Validar existencia de la cátedra
        catedra = self.session.get(CatedraAcademica, data.catedra_academica_id)
        if not catedra:
            raise NotFoundError("Cátedra académica no encontrada")

        # Validar cupos
        cupo_actual = self.session.query(Inscripcion).filter_by(
            catedra_academica_id=catedra.id, estado="activo"
        ).count()

        if cupo_actual >= catedra.cupos:
            raise PermissionDeniedError(f"No hay cupos disponibles en la cátedra {catedra.id}")

        # Verificar si ya existe
        existente = self.session.query(Inscripcion).filter_by(
            estudiante_id=data.estudiante_id, catedra_academica_id=catedra.id, estado="activo"
        ).first()

        if existente:
            raise PermissionDeniedError("El alumno ya está inscrito en esta cátedra")

        nueva = Inscripcion(
            estudiante_id=data.estudiante_id,
            catedra_academica_id=catedra.id,
            periodo_id=data.periodo_id,
            estado=data.estado or "activo"
        )

        self.session.add(nueva)
        self._commit_or_rollback()
        return self._to_response(nueva, InscripcionResponse)


    def cambiar_estado(self, inscripcion_id: int, nuevo_estado: str) -> InscripcionResponse:
        """Actualiza el estado de una inscripción"""
        insc = self._get_or_fail(Inscripcion, inscripcion_id)
        if nuevo_estado not in ["activo", "retirado", "aprobado"]:
            raise ValueError("Estado inválido")
        insc.estado = nuevo_estado
        self._commit_or_rollback()
        return self._to_response(insc, InscripcionResponse)

    def eliminar_inscripcion(self, inscripcion_id: int) -> bool:
        """Elimina la inscripción directamente (solo si no hay evaluaciones vinculadas, opcional)"""
        insc = self._get_or_fail(Inscripcion, inscripcion_id)
        self.session.delete(insc)
        return self._commit_or_rollback() is True

    def listar_por_alumno(self, estudiante_id: int) -> List[InscripcionResponse]:
        """Devuelve todas las inscripciones de un alumno"""
        inscripciones = self.session.query(Inscripcion).filter_by(
            estudiante_id=estudiante_id
        ).order_by(Inscripcion.fecha_inscripcion.desc()).all()

        return self._bulk_to_response(inscripciones, InscripcionResponse)

    def contar_estudiantes_en_catedra(self, catedra_id: int) -> int:
        """Cuenta el número de inscripciones activas en una cátedra académica"""
        return self.session.query(Inscripcion).filter_by(catedra_academica_id=catedra_id).count()

    def listar_por_catedra(self, catedra_id: int) -> List[InscripcionResponse]:
        """Devuelve todas las inscripciones activas en una cátedra"""
        inscripciones = self.session.query(Inscripcion).filter_by(
            catedra_academica_id=catedra_id
        ).order_by(Inscripcion.fecha_inscripcion.desc()).all()

        return self._bulk_to_response(inscripciones, InscripcionResponse)
    
    def obtener_inscripcion(self, inscripcion_id: int) -> InscripcionResponse:
        """Obtiene una inscripción específica"""
        insc = self._get_or_fail(Inscripcion, inscripcion_id)
        return self._to_response(insc, InscripcionResponse)