from typing import List

from app.database.controllers.db_controller import DatabaseController
from app.database.models import Usuario, ProfesorCatedra
from app.database.enums import Instrumento


class ProfesorCatedraController(DatabaseController):
    """Controlador para el modelo ProfesorCatedra"""
    
    def assign_instrument(self, profesor: Usuario, instrumento: Instrumento) -> bool:
        """Asigna un instrumento a un profesor"""
        if not profesor.is_teacher():
            return False

        exists = ProfesorCatedra.query.filter_by(
            profesor_id=profesor.id,
            instrumento=instrumento.value
        ).first()

        if exists:
            return True

        asignacion = ProfesorCatedra(
            profesor_id=profesor.id,
            instrumento=instrumento.value
        )

        self.session.add(asignacion)
        return self._commit_or_rollback() is True

    def remove_instrument(self, profesor: Usuario, instrumento: Instrumento) -> bool:
        """Elimina la asignación de un instrumento a un profesor"""
        asignacion = ProfesorCatedra.query.filter_by(
            profesor_id=profesor.id,
            instrumento=instrumento.value
        ).first()

        if not asignacion:
            return False

        self.session.delete(asignacion)
        return self._commit_or_rollback() is True

    def update_instrument(
        self,
        profesor: Usuario,
        old_instrument: Instrumento,
        new_instrument: Instrumento
    ) -> bool:
        """Actualiza la asignación de instrumento de un profesor"""
        asignacion = ProfesorCatedra.query.filter_by(
            profesor_id=profesor.id,
            instrumento=old_instrument.value
        ).first()

        if not asignacion:
            return False

        asignacion.instrumento = new_instrument.value
        return self._commit_or_rollback() is True

    def get_instruments_by_profesor(self, profesor: Usuario) -> List[Instrumento]:
        """Obtiene todos los instrumentos asignados a un profesor"""
        instrumentos = ProfesorCatedra.query.filter_by(
            profesor_id=profesor.id
        ).all()

        resultado: List[Instrumento] = []
        for instrumento in instrumentos:
            try:
                resultado.append(Instrumento(instrumento.instrumento))
            except ValueError as e:
                # Si algún instrumento guardado en DB no es válido para el Enum, lo ignoramos
                print(f"[WARN] Instrumento inválido en DB: {instrumento.instrumento}")
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