# This function is used to generate a seed for the academic database.
# It creates users, academic periods, academic chairs, enrollments, and grades.

from typing import Optional
from datetime import date
from flask import current_app

from app.database.enums import Catedra, Sexo, Role, Calificacion
from app.controllers import ControllerFactory

def generar_seed_academico() -> Optional[bool]:
    try:
        factory = ControllerFactory(current_user=None)

        user_ctrl = factory.get_user_controller()
        periodo_ctrl = factory.get_periodo_academico_controller()
        catedra_ctrl = factory.get_catedra_academica_controller()
        insc_ctrl = factory.get_inscripcion_controller()
        calif_ctrl = factory.get_calificacion_controller()
        profesor_catedra_ctrl = factory.get_profesor_catedra_controller()

        # 👥 Usuarios
        admin = user_ctrl.create_user("Super", "Admin", "admin@example.com", "123456", role=Role.SUPER_ADMIN, sexo=Sexo.NO_APLICA)
        profesor = user_ctrl.create_user("Luis", "González", "luis@example.com", "123456", role=Role.TEACHER, sexo=Sexo.MASCULINO)
        alumno = user_ctrl.create_user("Ana", "Ramírez", "ana@example.com", "123456", role=Role.STUDENT, sexo=Sexo.FEMENINO)
        alumno2 = user_ctrl.create_user("Pedro", "Pérez", "pedro@example.com", "123456", role=Role.STUDENT, sexo=Sexo.MASCULINO)
        alumno3 = user_ctrl.create_user("Juan", "Ilario", "juanilario@example.com", "123456", role=Role.STUDENT, sexo=Sexo.MASCULINO)

        # 📅 Período Académico
        periodo = periodo_ctrl.crear_periodo("2025-II", date(2025, 7, 1), date(2025, 12, 15))

        # 🎶 Cátedra Académica
        guitarra = catedra_ctrl.crear_catedra(Catedra.GUITARRA, periodo, grupo="A", profesor=profesor)
        profesor_catedra_ctrl.asignar_catedra(profesor, Catedra.GUITARRA)

        # 📝 Inscripción
        insc_ctrl.inscribir_alumno(alumno, guitarra)
        insc_ctrl.inscribir_alumno(alumno2, guitarra)
        insc_ctrl.inscribir_alumno(alumno3, guitarra)

        # 🏁 Calificaciones
        calif_ctrl.registrar_nota(alumno, guitarra, calificacion=Calificacion.AVANZADO, observaciones="Buen desempeño técnico.")
        calif_ctrl.registrar_nota(alumno2, guitarra, calificacion=Calificacion.CONSOLIDADO, observaciones="Necesita mejorar la técnica.")
        calif_ctrl.registrar_nota(alumno3, guitarra, calificacion=Calificacion.EN_PROCESO, observaciones="Requiere más práctica.")

        return True

    except Exception as e:
        current_app.logger.error(f"Error al generar el seed académico: {e}", exc_info=True)
        return None