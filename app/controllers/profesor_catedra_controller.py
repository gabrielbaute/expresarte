from typing import List, Optional

from flask import current_app
from app.controllers.db_controller import DatabaseController
from app.database.models import ProfesorCatedra, PeriodoAcademico, CatedraAcademica
from app.database.enums import Catedra
from app.schemas import (
    ProfesorCatedraCreate,
    ProfesorCatedraUpdate,
    ProfesorCatedraResponse,
    CatedraAcademicaResponse
)
from app.errors.exceptions import PermissionDeniedError, NotFoundError

class ProfesorCatedraController(DatabaseController):
    """Controlador para asignación de cátedras a profesores"""
    def __init__(self, db, current_user=None):
        super().__init__(db)
        self.current_user = current_user

    def asignar_catedra(self, data: ProfesorCatedraCreate) -> ProfesorCatedraResponse:
        """Asigna una cátedra a un profesor.
        
        Args:
            data (ProfesorCatedraCreate): Datos de la asignación.
        
        Returns:
            ProfesorCatedraResponse: La asignación realizada.
        
        Raises:
            PermissionDeniedError: Si ya existe una asignación para el profesor y cátedra.
        """
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
        """Actualiza los detalles de una asignación de cátedra a profesor.
        
        Args:
            asignacion_id (int): ID de la asignación.
            data (ProfesorCatedraUpdate): Datos actualizados de la asignación.
        
        Returns:
            ProfesorCatedraResponse: La asignación actualizada.
        """
        asignacion = self._get_or_fail(ProfesorCatedra, asignacion_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(asignacion, field, value)
        self._commit_or_rollback()
        return self._to_response(asignacion, ProfesorCatedraResponse)

    def get_catedras_by_profesor(self, profesor_id: int) -> List[ProfesorCatedraResponse]:
        """Obtiene todas las asignaciones de cátedras a un profesor.
        
        Args:
            profesor_id (int): ID del profesor.
        
        Returns:
            List[ProfesorCatedraResponse]: Lista de asignaciones del profesor.
        """
        registros = self.session.query(ProfesorCatedra).filter_by(profesor_id=profesor_id).all()
        return self._bulk_to_response(registros, ProfesorCatedraResponse)

    def get_catedra_academica(self, profesor_id: int, catedra: Catedra, periodo_id: int) -> Optional[CatedraAcademicaResponse]:
        """Obtiene una asignación de cátedra a profesor por profesor, cátedra y período.
        
        Args:
            profesor_id (int): ID del profesor.
            catedra (Catedra): Cátedra.
            periodo_id (int): ID del período.
        
        Returns:
            Optional[CatedraAcademicaResponse]: La asignación encontrada, si existe.
        """
        registro = self.session.query(CatedraAcademica).filter_by(
            profesor_id=profesor_id,
            catedra=catedra,
            periodo_id=periodo_id
        ).first()

        return self._to_response(registro, CatedraAcademicaResponse) if registro else None


    def obtener_por_id(self, asignacion_id: int) -> ProfesorCatedraResponse:
        """Obtiene una asignación de cátedra a profesor por su ID.
        
        Args:
            asignacion_id (int): ID de la asignación.
        
        Returns:
            ProfesorCatedraResponse: La asignación encontrada.
        """
        asignacion = self._get_or_fail(ProfesorCatedra, asignacion_id)
        return self._to_response(asignacion, ProfesorCatedraResponse)

    def eliminar_asignacion(self, profesor_id: int, catedra: Catedra) -> bool:
        """Elimina una asignación de cátedra a profesor.
        
        Args:
            profesor_id (int): ID del profesor.
            catedra (Catedra): Cátedra.
        
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        asignacion = self.session.query(ProfesorCatedra).filter_by(
            profesor_id=profesor_id,
            catedra=catedra
        ).first()

        if not asignacion:
            return False

        self.session.delete(asignacion)
        return self._commit_or_rollback() is True

    def get_students_by_catedra(self, profesor_id: int, catedra: str) -> List:
        """Obtiene los estudiantes de una cátedra concreta
        
        Args:
            profesor_id (int): ID del profesor.
            catedra (str): Cátedra.
        
        Returns:
            List: Lista de estudiantes.
        """
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
        """Obtiene todas las asignaciones de cátedras a profesores.
        
        Returns:
            List[ProfesorCatedraResponse]: Lista de todas las asignaciones.
        """
        registros = self.session.query(ProfesorCatedra).all()
        return self._bulk_to_response(registros, ProfesorCatedraResponse)