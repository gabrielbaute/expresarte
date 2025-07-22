from typing import List

from app.database.controllers.db_controller import DatabaseController
from app.database.models import Usuario, ProfesorCatedra
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

        asignacion.catedra = new_catedra
        return self._commit_or_rollback() is True

    def get_catedra_by_profesor(self, profesor: Usuario) -> List[Catedra]:
        """Obtiene todas las cátedras asignadas a un profesor"""
        registros = ProfesorCatedra.query.filter_by(profesor_id=profesor.id).all()

        resultado: List[Catedra] = []
        for registro in registros:
            try:
                resultado.append(Catedra(registro.catedra))
            except ValueError as e:
                print(f"[WARN] Cátedra inválida en DB: {registro.catedra} → {e}")
                continue
        return resultado

"""
    def get_instruments_by_profesor_string(self, profesor: Usuario) -> List[str]:
        # Obtiene todos los instrumentos asignados a un profesor
        instrumentos = ProfesorCatedra.query.filter_by(
            profesor_id=profesor.id
        ).all()
        
        return [i.instrumento for i in instrumentos]
"""