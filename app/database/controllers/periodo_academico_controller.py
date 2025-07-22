from datetime import date
from typing import List, Optional

from flask import current_app
from app.database.controllers.db_controller import DatabaseController
from app.database.models import PeriodoAcademico


class PeriodoAcademicoController(DatabaseController):
    """Controlador para gestionar períodos académicos"""

    def crear_periodo(self, nombre: str, fecha_inicio: date, fecha_fin: date) -> Optional[PeriodoAcademico]:
        """Crea un nuevo período académico"""
        if fecha_inicio >= fecha_fin:
            current_app.logger.warning("Las fechas del período son inválidas")
            return None

        existente = PeriodoAcademico.query.filter_by(nombre=nombre).first()
        if existente:
            current_app.logger.info(f"Ya existe el período académico {nombre}")
            return None

        nuevo = PeriodoAcademico(nombre=nombre, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        self.session.add(nuevo)

        if self._commit_or_rollback() is True:
            return nuevo
        return None

    def listar_periodos(self, solo_activos: bool = False) -> List[PeriodoAcademico]:
        """Lista todos los períodos académicos"""
        query = PeriodoAcademico.query
        if solo_activos:
            query = query.filter_by(activo=True)
        return query.order_by(PeriodoAcademico.fecha_inicio.desc()).all()

    def activar_periodo(self, periodo_id: int) -> bool:
        """Marca un período como activo"""
        periodo = PeriodoAcademico.query.get(periodo_id)
        if not periodo:
            return False
        periodo.activo = True
        return self._commit_or_rollback() is True

    def desactivar_periodo(self, periodo_id: int) -> bool:
        """Desactiva un período académico"""
        periodo = PeriodoAcademico.query.get(periodo_id)
        if not periodo:
            return False
        periodo.activo = False
        return self._commit_or_rollback() is True

    def obtener_periodo_por_nombre(self, nombre: str) -> Optional[PeriodoAcademico]:
        """Devuelve el período académico con ese nombre si existe"""
        return PeriodoAcademico.query.filter_by(nombre=nombre).first()
