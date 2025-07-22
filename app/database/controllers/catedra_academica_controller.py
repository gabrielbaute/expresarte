from typing import List, Optional

from flask import current_app
from app.database.controllers.db_controller import DatabaseController
from app.database.models import CatedraAcademica, Usuario, PeriodoAcademico
from app.database.enums import Catedra


class CatedraAcademicaController(DatabaseController):
    """Controlador para gestión de cátedras académicas por período"""

    def crear_catedra(
        self,
        nombre_catedra: Catedra,
        periodo: PeriodoAcademico,
        grupo: str,
        profesor: Optional[Usuario] = None,
        cupos: int = 20
    ) -> Optional[CatedraAcademica]:
        """Crea una nueva cátedra académica en un período dado"""
        if not periodo:
            current_app.logger.warning("El período académico es requerido")
            return None

        if profesor and not profesor.is_teacher():
            current_app.logger.warning(f"El usuario no es profesor válido → {profesor.email}")
            return None

        existente = CatedraAcademica.query.filter_by(
            catedra=nombre_catedra.value,
            periodo_id=periodo.id,
            grupo=grupo
        ).first()

        if existente:
            current_app.logger.info(f"La cátedra {nombre_catedra.value} ya existe en el grupo {grupo} del período {periodo.nombre}")
            return None

        nueva = CatedraAcademica(
            catedra=nombre_catedra.value,
            periodo_id=periodo.id,
            grupo=grupo,
            profesor_id=profesor.id if profesor else None,
            cupos=cupos
        )

        self.session.add(nueva)
        return nueva if self._commit_or_rollback() is True else None

    def asignar_profesor(self, catedra_id: int, profesor: Usuario) -> bool:
        """Asigna o actualiza el profesor responsable de una cátedra"""
        catedra = CatedraAcademica.query.get(catedra_id)
        if not catedra or not profesor or not profesor.is_teacher():
            return False

        catedra.profesor_id = profesor.id
        return self._commit_or_rollback() is True

    def listar_por_periodo(self, periodo: PeriodoAcademico) -> List[CatedraAcademica]:
        """Devuelve todas las cátedras asociadas a un período académico"""
        return CatedraAcademica.query.filter_by(periodo_id=periodo.id).order_by(CatedraAcademica.grupo).all()

    def listar_por_profesor(self, profesor: Usuario) -> List[CatedraAcademica]:
        """Devuelve todas las cátedras asignadas a un profesor"""
        return CatedraAcademica.query.filter_by(profesor_id=profesor.id).order_by(CatedraAcademica.periodo_id.desc()).all()

    def eliminar_catedra(self, catedra_id: int) -> bool:
        """Elimina una cátedra académica"""
        catedra = CatedraAcademica.query.get(catedra_id)
        if not catedra:
            return False
        self.session.delete(catedra)
        return self._commit_or_rollback() is True

    def obtener_por_id(self, catedra_id: int) -> Optional[CatedraAcademica]:
        """Obtiene una cátedra por su ID"""
        return CatedraAcademica.query.get(catedra_id)
