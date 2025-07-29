from flask import current_app
from typing import List

from app.database.controllers.db_controller import DatabaseController
from app.database.models import Usuario, ProfesorCatedra, CatedraAcademica, PeriodoAcademico
from app.database.enums import Catedra


class ProfesorCatedraController(DatabaseController):
    """Controlador para el modelo ProfesorCatedra"""
    
    def asignar_catedra(self, profesor: Usuario, catedra: Catedra) -> bool:
        """Asigna una cátedra a un profesor"""
        if not profesor.is_teacher():
            return False

        exists = ProfesorCatedra.query.filter_by(
            profesor_id=profesor.id,
            catedra=catedra.value
        ).first()

        if exists:
            return True

        asignacion = ProfesorCatedra(
            profesor_id=profesor.id,
            catedra=catedra.value
        )

        self.session.add(asignacion)
        return self._commit_or_rollback() is True

    def remove_catedra(self, profesor: Usuario, catedra: Catedra) -> bool:
        """Elimina la asignación de una cátedra a un profesor"""
        asignacion = ProfesorCatedra.query.filter_by(
            profesor_id=profesor.id,
            catedra=catedra.value
        ).first()

        if not asignacion:
            return False

        self.session.delete(asignacion)
        return self._commit_or_rollback() is True

    def update_catedra(
        self,
        profesor: Usuario,
        old_catedra: Catedra,
        new_catedra: Catedra
    ) -> bool:
        """Actualiza la asignación de cátedra de un profesor"""
        asignacion = ProfesorCatedra.query.filter_by(
            profesor_id=profesor.id,
            catedra=old_catedra.value
        ).first()

        if not asignacion:
            return False

        asignacion.catedra = new_catedra.value
        return self._commit_or_rollback() is True

    def get_catedra_by_profesor(self, profesor: Usuario) -> List[Catedra]:
        """Obtiene todas las cátedras asignadas a un profesor"""
        registros = ProfesorCatedra.query.filter_by(profesor_id=profesor.id).all()

        resultado: List[Catedra] = []
        for registro in registros:
            if registro.catedra not in Catedra.to_list():
                current_app.logger.warning(f"Cátedra desconocida en DB: {registro.catedra}")
                continue
            try:
                resultado.append(Catedra.from_label(registro.catedra))
            except ValueError as e:
                current_app.logger.warning(f"Cátedra desconocida en DB: {registro.catedra}")
        return resultado

    def get_catedra_dicts_by_profesor(self, profesor: Usuario) -> List[dict]:
        """Devuelve una lista de diccionarios con todos los profesores y cátedras"""
        catedras = self.get_catedra_by_profesor(profesor)
        return [c.to_dict() for c in catedras]
    
    def get_students_by_profesor(self, profesor: Usuario) -> List[Usuario]:
        """Obtiene todos los estudiantes asignados a un profesor"""
        catedras = self.get_catedra_by_profesor(profesor)
        estudiantes = []
        
        for catedra in catedras:
            estudiantes.extend(catedra.get_students())
        
        return estudiantes

    def get_students_by_catedra(self, profesor: Usuario, catedra: Catedra) -> List[Usuario]:
        """Devuelve la lista de estudiantes inscritos activamente en la cátedra de un profesor"""
        # Validar que el profesor tenga asignada esta cátedra
        catedras_asignadas = self.get_catedra_by_profesor(profesor)
        if catedra not in catedras_asignadas:
            current_app.logger.info(f"El profesor no tiene asignada la cátedra: {catedra}")
            return []

        # Buscar todas las CatedraAcademica registradas en ese período activo
        periodo = PeriodoAcademico.query.filter_by(activo=True).first()
        if not periodo:
            current_app.logger.warning("No hay período académico activo")
            return []

        registros = CatedraAcademica.query.filter_by(
            profesor_id=profesor.id,
            catedra=catedra.value,
            periodo_id=periodo.id
        ).all()

        estudiantes: List[Usuario] = []

        for ca in registros:
            inscripciones = ca.inscripciones.filter_by(estado="activo").all()
            estudiantes.extend([i.student for i in inscripciones if i.student and i.student.is_student()])

        return estudiantes



"""
    def get_instruments_by_profesor_string(self, profesor: Usuario) -> List[str]:
        # Obtiene todos los instrumentos asignados a un profesor
        instrumentos = ProfesorCatedra.query.filter_by(
            profesor_id=profesor.id
        ).all()
        
        return [i.instrumento for i in instrumentos]
"""