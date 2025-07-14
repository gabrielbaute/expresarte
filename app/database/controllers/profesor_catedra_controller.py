# controllers/profesor_catedra_controller.py
from app.database.db_config import db
from app.database.models import Usuario, ProfesorCatedra
from app.database.controllers.db_controller import DatabaseController


class ProfesorCatedraController(DatabaseController):
    """Controlador para el modelo ProfesorCatedra"""
    
    def assign_instrument(self, profesor: Usuario, instrumento: str) -> bool:
        """Asigna un instrumento a un profesor"""
        if not profesor.is_teacher():
            return False

        exists = ProfesorCatedra.query.filter_by(
            profesor_id=profesor.id,
            instrumento=instrumento
        ).first()

        if exists:
            return True

        asignacion = ProfesorCatedra(
            profesor_id=profesor.id,
            instrumento=instrumento
        )

        self.session.add(asignacion)
        return self._commit_or_rollback() is True

    def remove_instrument(self, profesor: Usuario, instrumento: str) -> bool:
        """Elimina la asignación de un instrumento a un profesor"""
        asignacion = ProfesorCatedra.query.filter_by(
            profesor_id=profesor.id,
            instrumento=instrumento
        ).first()

        if not asignacion:
            return False

        self.session.delete(asignacion)
        return self._commit_or_rollback() is True

    def update_instrument(
        self,
        profesor: Usuario,
        old_instrument: str,
        new_instrument: str
    ) -> bool:
        """Actualiza la asignación de instrumento de un profesor"""
        asignacion = ProfesorCatedra.query.filter_by(
            profesor_id=profesor.id,
            instrumento=old_instrument
        ).first()

        if not asignacion:
            return False

        asignacion.instrumento = new_instrument
        return self._commit_or_rollback() is True

    def get_instruments_by_profesor(self, profesor: Usuario) -> list[str]:
        """Obtiene todos los instrumentos asignados a un profesor"""
        instrumentos = ProfesorCatedra.query.filter_by(
            profesor_id=profesor.id
        ).all()
        
        return [i.instrumento for i in instrumentos]