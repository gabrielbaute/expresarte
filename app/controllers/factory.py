from app.database import db
from app.controllers.profesor_catedra_controller import ProfesorCatedraController
from app.controllers.calificacion_controller import CalificacionController
from app.controllers.inscripcion_controller import InscripcionController
from app.controllers.catedra_academica_controller import CatedraAcademicaController
from app.controllers.periodo_academico_controller import PeriodoAcademicoController
from app.controllers.user_controller import UserController

class ControllerFactory:
    """Fábrica para crear controladores de la aplicación con acceso opcional al usuario actual."""
    
    def __init__(self, db_instance=db, current_user=None):
        if not hasattr(db_instance, "session"):
            raise ValueError("El objeto db no parece ser una instancia válida de SQLAlchemy")
        
        self.db = db_instance
        self.current_user = current_user

    def get_user_controller(self):
        """Crea una instancia de UserController con el usuario actual.
        
        Returns:
            UserController: Instancia del controlador de usuarios.
        """
        return UserController(self.db, current_user=self.current_user)

    def get_catedra_academica_controller(self):
        """Crea una instancia de CatedraAcademicaController con el usuario actual.
        
        Returns:
            CatedraAcademicaController: Instancia del controlador de cátedras académicas.
        """
        return CatedraAcademicaController(self.db, current_user=self.current_user)

    def get_periodo_academico_controller(self):
        """Crea una instancia de PeriodoAcademicoController con el usuario actual.
        
        Returns:
            PeriodoAcademicoController: Instancia del controlador de períodos académicos.
        """
        return PeriodoAcademicoController(self.db, current_user=self.current_user)

    def get_profesor_catedra_controller(self):
        """Crea una instancia de ProfesorCatedraController con el usuario actual.
        
        Returns:
            ProfesorCatedraController: Instancia del controlador de asignaciones de cátedras a profesores.
        """
        return ProfesorCatedraController(self.db, current_user=self.current_user)

    def get_calificacion_controller(self):
        """Crea una instancia de CalificacionController con el usuario actual.
        
        Returns:
            CalificacionController: Instancia del controlador de calificaciones.
        """
        return CalificacionController(self.db, current_user=self.current_user)

    def get_inscripcion_controller(self):
        """Crea una instancia de InscripcionController con el usuario actual.
        
        Returns:
            InscripcionController: Instancia del controlador de inscripciones.
        """
        return InscripcionController(self.db, current_user=self.current_user)
