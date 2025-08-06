from typing import Optional, List

from app.controllers.db_controller import DatabaseController
from app.database.models import CatedraAcademica
from app.database.enums import Catedra
from app.schemas.catedra_periodo import (
    CatedraAcademicaCreate,
    CatedraAcademicaUpdate,
    CatedraAcademicaResponse
)
from app.errors.exceptions import NotFoundError, PermissionDeniedError

class CatedraAcademicaController(DatabaseController):
    """Controlador para gestión de cátedras académicas por período"""
    def __init__(self, db, current_user=None):
        super().__init__(db)
        self.current_user = current_user

    def crear_catedra(self, data: CatedraAcademicaCreate) -> CatedraAcademicaResponse:
        """Crea una nueva cátedra académica."""
        existente = self.session.query(CatedraAcademica).filter_by(
            catedra=data.catedra,
            periodo_id=data.periodo_id,
            grupo=data.grupo
        ).first()

        if existente:
            raise PermissionDeniedError(
                f"La cátedra {data.catedra} ya existe en el grupo {data.grupo} del período ID {data.periodo_id}"
            )

        nueva = CatedraAcademica(**data.model_dump())
        self.session.add(nueva)
        self._commit_or_rollback()
        return self._to_response(nueva, CatedraAcademicaResponse)

    def asignar_profesor(self, catedra_id: int, profesor_id: int) -> CatedraAcademicaResponse:
        """Asigna un profesor a una cátedra académica."""
        catedra = self._get_or_fail(CatedraAcademica, catedra_id)
        catedra.profesor_id = profesor_id
        self._commit_or_rollback()
        return self._to_response(catedra, CatedraAcademicaResponse)

    def listar_por_periodo(self, periodo_id: int) -> List[CatedraAcademicaResponse]:
        """Lista todas las cátedras académicas de un período específico."""
        catedras = self.session.query(CatedraAcademica).filter_by(periodo_id=periodo_id).order_by(
            CatedraAcademica.grupo
        ).all()
        return self._bulk_to_response(catedras, CatedraAcademicaResponse)

    def listar_por_profesor(self, profesor_id: int) -> List[CatedraAcademicaResponse]:
        """Lista todas las cátedras académicas asignadas a un profesor específico."""
        catedras = self.session.query(CatedraAcademica).filter_by(profesor_id=profesor_id).order_by(
            CatedraAcademica.periodo_id.desc()
        ).all()
        return self._bulk_to_response(catedras, CatedraAcademicaResponse)

    def eliminar_catedra(self, catedra_id: int) -> bool:
        """Elimina una cátedra académica por su ID."""
        catedra = self._get_or_fail(CatedraAcademica, catedra_id)
        self.session.delete(catedra)
        return self._commit_or_rollback() is True

    def obtener_por_id(self, catedra_id: int) -> CatedraAcademicaResponse:
        """Obtiene una cátedra académica por su ID."""
        catedra = self._get_or_fail(CatedraAcademica, catedra_id)
        return self._to_response(catedra, CatedraAcademicaResponse)

    def actualizar_catedra(self, catedra_id: int, data: CatedraAcademicaUpdate) -> CatedraAcademicaResponse:
        """Actualiza los detalles de una cátedra académica."""
        catedra = self._get_or_fail(CatedraAcademica, catedra_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(catedra, field, value)
        self._commit_or_rollback()
        return self._to_response(catedra, CatedraAcademicaResponse)
