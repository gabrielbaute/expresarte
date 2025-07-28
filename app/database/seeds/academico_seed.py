from typing import Optional
from datetime import date
from flask import current_app

from app.database.enums import Catedra
from app.database.controllers import (
    UserController,
    PeriodoAcademicoController,
    CatedraAcademicaController, 
    InscripcionController,
    CalificacionController,
    ProfesorCatedraController
)

def generar_seed_academico() -> Optional[bool]:
    
    # Cargar controladores:
    user_ctrl = UserController()
    periodo_ctrl = PeriodoAcademicoController()
    catedra_ctrl = CatedraAcademicaController()
    insc_ctrl = InscripcionController()
    calif_ctrl = CalificacionController()
    profesor_catedra_ctrl = ProfesorCatedraController()

    try:
        # 👥 Usuarios
        admin = user_ctrl.create_user("Super", "Admin", "admin@example.com", "123456", role="super_admin", sexo="N/A")
        profesor = user_ctrl.create_user("Luis", "González", "luis@example.com", "123456", role="teacher", sexo="M")
        alumno = user_ctrl.create_user("Ana", "Ramírez", "ana@example.com", "123456", role="student", sexo="F")

        # 📅 Período Académico
        periodo = periodo_ctrl.crear_periodo("2025-II", date(2025, 7, 1), date(2025, 12, 15))

        # 🎶 Cátedra Académica
        guitarra = catedra_ctrl.crear_catedra(Catedra.GUITARRA, periodo, grupo="A", profesor=profesor)
        profesor_catedra_ctrl.asignar_catedra(profesor, Catedra.GUITARRA)

        # 📝 Inscripción
        inscripcion = insc_ctrl.inscribir_alumno(alumno, guitarra)

        # 🏁 Calificación
        calificacion = calif_ctrl.registrar_nota(alumno, guitarra, nota=16.5, observaciones="Buen desempeño técnico.")

        return True
    
    except Exception as e:
        current_app.logger.error(f"Error al generar el seed académico: {e}", exc_info=True)
        return None