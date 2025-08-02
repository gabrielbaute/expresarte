from datetime import date
from typing import List, Optional

from app.controllers.db_controller import DatabaseController
from app.database.models import PeriodoAcademico
from app.schemas import PeriodoAcademicoCreate, PeriodoAcademicoUpdate, PeriodoAcademicoResponse
from app.errors import NotFoundError
from sqlalchemy.exc import IntegrityError


class PeriodoAcademicoController(DatabaseController):
    """Controlador para gestión de períodos académicos"""
    def __init__(self, db, current_user=None):
        super().__init__(db)
        self.current_user = current_user

    def crear_periodo(self, data: PeriodoAcademicoCreate) -> PeriodoAcademicoResponse:
        if data.fecha_inicio >= data.fecha_fin:
            raise ValueError("La fecha de inicio debe ser menor a la fecha de fin.")

        existente = self.session.query(PeriodoAcademico).filter_by(nombre=data.nombre).first()
        if existente:
            raise IntegrityError(None, None, f"Ya existe un período académico con nombre '{data.nombre}'.")

        nuevo = PeriodoAcademico(
            nombre=data.nombre,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=data.fecha_fin
        )
        self.session.add(nuevo)
        self._commit_or_rollback()
        return self._to_response(nuevo, PeriodoAcademicoResponse)

    def listar_periodos(self, solo_activos: bool = False) -> List[PeriodoAcademicoResponse]:
        query = self.session.query(PeriodoAcademico)
        if solo_activos:
            query = query.filter_by(activo=True)
        periodos = query.order_by(PeriodoAcademico.fecha_inicio.desc()).all()
        return self._bulk_to_response(periodos, PeriodoAcademicoResponse)

    def activar_periodo(self, periodo_id: int) -> PeriodoAcademicoResponse:
        periodo = self._get_or_fail(PeriodoAcademico, periodo_id)
        periodo.activo = True
        self._commit_or_rollback()
        return self._to_response(periodo, PeriodoAcademicoResponse)

    def desactivar_periodo(self, periodo_id: int) -> PeriodoAcademicoResponse:
        periodo = self._get_or_fail(PeriodoAcademico, periodo_id)
        periodo.activo = False
        self._commit_or_rollback()
        return self._to_response(periodo, PeriodoAcademicoResponse)

    def obtener_periodo_por_nombre(self, nombre: str) -> Optional[PeriodoAcademicoResponse]:
        periodo = self.session.query(PeriodoAcademico).filter_by(nombre=nombre).first()
        return self._to_response(periodo, PeriodoAcademicoResponse) if periodo else None

    def delete_periodo(self, periodo_id: int) -> bool:
        periodo = self._get_or_fail(PeriodoAcademico, periodo_id)
        self.session.delete(periodo)
        return self._commit_or_rollback() is True

    def update_periodo(self, periodo_id: int, data: PeriodoAcademicoUpdate) -> PeriodoAcademicoResponse:
        periodo = self._get_or_fail(PeriodoAcademico, periodo_id)

        valores = data.model_dump(exclude_unset=True)

        if "fecha_inicio" in valores and "fecha_fin" in valores:
            if valores["fecha_inicio"] >= valores["fecha_fin"]:
                raise ValueError("La fecha de inicio debe ser menor a la fecha de fin.")

        for field, value in valores.items():
            setattr(periodo, field, value)

        self._commit_or_rollback()
        return self._to_response(periodo, PeriodoAcademicoResponse)
