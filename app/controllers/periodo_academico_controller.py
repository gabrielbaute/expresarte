import logging
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
        self.logger = logging.getLogger(f"[{self.__class__.__name__}]")

    def crear_periodo(self, data: PeriodoAcademicoCreate) -> PeriodoAcademicoResponse:
        """Crea un nuevo período académico.

        Args:
            data (PeriodoAcademicoCreate): Datos del período académico.

        Returns:
            PeriodoAcademicoResponse: El período académico creado.
        """
        if data.fecha_inicio >= data.fecha_fin:
            self.logger.warning("La fecha de inicio debe ser menor a la fecha de fin.")
            raise ValueError("La fecha de inicio debe ser menor a la fecha de fin.")

        existente = self.session.query(PeriodoAcademico).filter_by(nombre=data.nombre).first()
        if existente:
            self.logger.error(f"Ya existe un período académico con nombre '{data.nombre}'.")
            raise IntegrityError(None, None, f"Ya existe un período académico con nombre '{data.nombre}'.")

        nuevo = PeriodoAcademico(
            nombre=data.nombre,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=data.fecha_fin
        )
        self.session.add(nuevo)
        self._commit_or_rollback()
        self.logger.info(f"Periodo académico creado: {nuevo}")
        return self._to_response(nuevo, PeriodoAcademicoResponse)

    def listar_periodos(self, solo_activos: bool = False) -> List[PeriodoAcademicoResponse]:
        """Lista todos los períodos académicos.
        
        Args:
            solo_activos (bool): Si True, solo devuelve los períodos activos.
        
        Returns:
            List[PeriodoAcademicoResponse]: Lista de períodos académicos.
        """
        query = self.session.query(PeriodoAcademico)
        if solo_activos:
            query = query.filter_by(activo=True)
        periodos = query.order_by(PeriodoAcademico.fecha_inicio.desc()).all()
        self.logger.info(f"Lista de períodos académicos: {periodos}")
        return self._bulk_to_response(periodos, PeriodoAcademicoResponse)

    def activar_periodo(self, periodo_id: int) -> PeriodoAcademicoResponse:
        """Activa un período académico.
        
        Args:
            periodo_id (int): ID del período a activar.
        
        Returns:
            PeriodoAcademicoResponse: El período académico activado.
        """
        self.session.query(PeriodoAcademico).update({PeriodoAcademico.activo: False}) # <--- Experimental, para evitar que haya más de un período activo a la vez
        periodo = self._get_or_fail(PeriodoAcademico, periodo_id)
        periodo.activo = True
        self._commit_or_rollback()
        self.logger.info(f"Periodo académico activado: {periodo}")
        return self._to_response(periodo, PeriodoAcademicoResponse)

    def desactivar_periodo(self, periodo_id: int) -> PeriodoAcademicoResponse:
        """Desactiva un período académico.
        
        Args:
            periodo_id (int): ID del período a desactivar.
        
        Returns:
            PeriodoAcademicoResponse: El período académico desactivado.
        """
        periodo = self._get_or_fail(PeriodoAcademico, periodo_id)
        periodo.activo = False
        self._commit_or_rollback()
        self.logger.info(f"Periodo académico desactivado: {periodo}")
        return self._to_response(periodo, PeriodoAcademicoResponse)

    def obtener_periodo_por_nombre(self, nombre: str) -> Optional[PeriodoAcademicoResponse]:
        """Obtiene un período académico por su nombre.
        
        Args:
            nombre (str): Nombre del período.
        
        Returns:
            Optional[PeriodoAcademicoResponse]: El período académico encontrado, si existe.
        """
        periodo = self.session.query(PeriodoAcademico).filter_by(nombre=nombre).first()
        self.logger.info(f"Periodo académico encontrado: {periodo}")
        return self._to_response(periodo, PeriodoAcademicoResponse) if periodo else None

    def get_active_periodo(self) -> Optional[PeriodoAcademicoResponse]:
        """Devuelve el período académico marcado como activo, si existe
        
        Returns:
            Optional[PeriodoAcademicoResponse]: El período académico activo, si existe.
        """
        activo = self.session.query(PeriodoAcademico).filter_by(activo=True).first()
        self.logger.info(f"Periodo académico activo: {activo}")
        return self._to_response(activo, PeriodoAcademicoResponse) if activo else None

    def delete_periodo(self, periodo_id: int) -> bool:
        """Elimina un período académico.

        Args:
            periodo_id (int): ID del período a eliminar.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        periodo = self._get_or_fail(PeriodoAcademico, periodo_id)
        self.session.delete(periodo)
        self.logger.info(f"Periodo académico eliminado: {periodo}")
        return self._commit_or_rollback() is True

    def update_periodo(self, periodo_id: int, data: PeriodoAcademicoUpdate) -> PeriodoAcademicoResponse:
        """Actualiza los detalles de un período académico.
        
        Args:
            periodo_id (int): ID del período a actualizar.
            data (PeriodoAcademicoUpdate): Datos actualizados del período.
        
        Returns:
            PeriodoAcademicoResponse: El período académico actualizado.
        
        Raises:
            ValueError: Si la fecha de inicio es mayor o igual a la fecha de fin.
        """
        periodo = self._get_or_fail(PeriodoAcademico, periodo_id)

        valores = data.model_dump(exclude_unset=True)

        if "fecha_inicio" in valores and "fecha_fin" in valores:
            if valores["fecha_inicio"] >= valores["fecha_fin"]:
                raise ValueError("La fecha de inicio debe ser menor a la fecha de fin.")

        for field, value in valores.items():
            setattr(periodo, field, value)

        self._commit_or_rollback()
        self.logger.info(f"Periodo académico actualizado: {periodo}")
        return self._to_response(periodo, PeriodoAcademicoResponse)
