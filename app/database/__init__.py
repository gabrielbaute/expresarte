from app.database.db_config import db, init_db
from app.database.models import Usuario, ProfesorCatedra, Calificacion, Inscripcion, CatedraAcademica, PeriodoAcademico
from app.database.enums import Role, Permission, ROLE_HIERARCHY, ROLE_PERMISSIONS
from app.database.controllers import (
    UserController, 
    ProfesorCatedraController,
    PeriodoAcademicoController, 
    CatedraAcademicaController, 
    InscripcionController, 
    CalificacionController
    )
from app.database.seeds.academico_seed import generar_seed_academico