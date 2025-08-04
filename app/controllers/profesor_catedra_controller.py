from typing import List

from flask import current_app
from app.controllers.db_controller import DatabaseController
from app.database.models import ProfesorCatedra, PeriodoAcademico, CatedraAcademica
from app.database.enums import Catedra
from app.schemas.profesor_catedra import (
    ProfesorCatedraCreate,
    ProfesorCatedraUpdate,
    ProfesorCatedraResponse
)
from app.errors.exceptions import PermissionDeniedError, NotFoundError

class ProfesorCatedraController(DatabaseController):
    """Controlador para asignación de cátedras a profesores"""
    def __init__(self, db, current_user=None):
        super().__init__(db)
        self.current_user = current_user

    def asignar_catedra(self, data: ProfesorCatedraCreate) -> ProfesorCatedraResponse:
        existente = self.session.query(ProfesorCatedra).filter_by(
            profesor_id=data.profesor_id,
            catedra=data.catedra
        ).first()

        if existente:
            return self._to_response(existente, ProfesorCatedraResponse)

        nueva = ProfesorCatedra(**data.model_dump())
        self.session.add(nueva)
        self._commit_or_rollback()
        return self._to_response(nueva, ProfesorCatedraResponse)

    def actualizar_asignacion(self, asignacion_id: int, data: ProfesorCatedraUpdate) -> ProfesorCatedraResponse:
        asignacion = self._get_or_fail(ProfesorCatedra, asignacion_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(asignacion, field, value)
        self._commit_or_rollback()
        return self._to_response(asignacion, ProfesorCatedraResponse)

    def get_catedras_by_profesor(self, profesor_id: int) -> List[ProfesorCatedraResponse]:
        registros = self.session.query(ProfesorCatedra).filter_by(profesor_id=profesor_id).all()
        return self._bulk_to_response(registros, ProfesorCatedraResponse)


    def obtener_por_id(self, asignacion_id: int) -> ProfesorCatedraResponse:
        asignacion = self._get_or_fail(ProfesorCatedra, asignacion_id)
        return self._to_response(asignacion, ProfesorCatedraResponse)

    def eliminar_asignacion(self, profesor_id: int, catedra: Catedra) -> bool:
        asignacion = self.session.query(ProfesorCatedra).filter_by(
            profesor_id=profesor_id,
            catedra=catedra
        ).first()

        if not asignacion:
            return False

        self.session.delete(asignacion)
        return self._commit_or_rollback() is True

    def get_students_by_catedra(self, profesor_id: int, catedra: str) -> List:
        periodo = self.session.query(PeriodoAcademico).filter_by(activo=True).first()
        if not periodo:
            current_app.logger.warning("No hay período académico activo")
            return []

        registros = self.session.query(CatedraAcademica).filter_by(
            profesor_id=profesor_id,
            catedra=catedra,
            periodo_id=periodo.id
        ).all()

        estudiantes = []
        for ca in registros:
            inscripciones = ca.inscripciones.filter_by(estado="activo").all()
            estudiantes.extend([
                i.student for i in inscripciones if i.student and i.student.is_student()
            ])

        return estudiantes

    def get_all_catedras(self) -> List[ProfesorCatedraResponse]:
        registros = self.session.query(ProfesorCatedra).all()
        return self._bulk_to_response(registros, ProfesorCatedraResponse)