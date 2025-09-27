# This function is used to generate a seed for the academic database.
# It creates users, academic periods, academic chairs, enrollments, and grades.

from typing import Optional
from datetime import date
from flask import current_app
from werkzeug.security import generate_password_hash

from app.database.enums import Catedra, Sexo, Role, Calificacion, EstadoInscripcion
from app.controllers import ControllerFactory
from app.schemas import UserCreate, PeriodoAcademicoCreate, CatedraAcademicaCreate, ProfesorCatedraCreate, InscripcionCreate, CalificacionCreate

def generar_seed_academico() -> Optional[bool]:
    """Genera datos de prueba para la base de datos académica.
    
    Returns:
        Optional[bool]: True si la generación fue exitosa, False en caso contrario.
    """
    try:
        factory = ControllerFactory(current_user=None)

        user_ctrl = factory.get_user_controller()
        periodo_ctrl = factory.get_periodo_academico_controller()
        catedra_ctrl = factory.get_catedra_academica_controller()
        insc_ctrl = factory.get_inscripcion_controller()
        calif_ctrl = factory.get_calificacion_controller()
        profesor_catedra_ctrl = factory.get_profesor_catedra_controller()
        
        DEFAULT_PASSWORD = "123456"
        
        admin2 = UserCreate(
            primer_nombre="Super",
            primer_apellido="Admin",
            email="admin2@example.com",
            password_hash=DEFAULT_PASSWORD,
            role=Role.ADMIN,
            sexo=Sexo.MASCULINO)

        # 👥 Usuarios (usando helper)
        admin = user_ctrl.create_user(admin2)
        profesor = user_ctrl.create_user(UserCreate(primer_nombre="Luis", primer_apellido="González", email="luis@example.com", password_hash=DEFAULT_PASSWORD, role=Role.TEACHER, sexo=Sexo.MASCULINO))
        alumno = user_ctrl.create_user(UserCreate(primer_nombre="Ana", primer_apellido="Ramírez", email="ana@example.com", password_hash=DEFAULT_PASSWORD, role=Role.STUDENT, sexo=Sexo.FEMENINO))
        alumno2 = user_ctrl.create_user(UserCreate(primer_nombre="Pedro", primer_apellido="Pérez", email="pedro@example.com", password_hash=DEFAULT_PASSWORD, role=Role.STUDENT, sexo=Sexo.MASCULINO))
        alumno3 = user_ctrl.create_user(UserCreate(primer_nombre="Juan", primer_apellido="Ilario", email="juan@exanoke.com", password_hash=DEFAULT_PASSWORD, role=Role.STUDENT, sexo=Sexo.MASCULINO))
        alumno4 = user_ctrl.create_user(UserCreate(primer_nombre="Carlos", primer_apellido="Santana", email="carlos@example.com", password_hash=DEFAULT_PASSWORD, role=Role.STUDENT, sexo=Sexo.MASCULINO))
        alumno5 = user_ctrl.create_user(UserCreate(primer_nombre="Antonio", primer_apellido="Machado", email="antoniomachado@exanoke.com", password_hash=DEFAULT_PASSWORD, role=Role.STUDENT, sexo=Sexo.MASCULINO))
        alumno6 = user_ctrl.create_user(UserCreate(primer_nombre="Jesus", primer_apellido="Calvo", email="jesus@exanoke.com", password_hash=DEFAULT_PASSWORD, role=Role.STUDENT, sexo=Sexo.MASCULINO))
        alumno7 = user_ctrl.create_user(UserCreate(primer_nombre="Catire", primer_apellido="Florentino", email="florentino@exanoke.com", password_hash=DEFAULT_PASSWORD, role=Role.STUDENT, sexo=Sexo.MASCULINO))


        # 📅 Período Académico
        periodo = periodo_ctrl.crear_periodo(PeriodoAcademicoCreate(nombre="2025-II", fecha_inicio=date(2025, 7, 1), fecha_fin=date(2025, 12, 15)))

        # 🎶 Cátedra Académica
        catedra_guitarra = CatedraAcademicaCreate(
            profesor_id=profesor.id,
            catedra=Catedra.GUITARRA.value,
            periodo_id=periodo.id,
            grupo="A",
            cupos=20
        )
        guitarra = catedra_ctrl.crear_catedra(catedra_guitarra)
        profesor_guitarra = ProfesorCatedraCreate(
            profesor_id=profesor.id,
            catedra=Catedra.GUITARRA
        )
        profesor_catedra_ctrl.asignar_catedra(profesor_guitarra)

        # 📝 Inscripción
        insc_ctrl.inscribir_alumno(InscripcionCreate(estudiante_id=alumno.id, catedra_academica_id=guitarra.id, periodo_id=periodo.id, estado=EstadoInscripcion.ACTIVO))
        insc_ctrl.inscribir_alumno(InscripcionCreate(estudiante_id=alumno2.id, catedra_academica_id=guitarra.id, periodo_id=periodo.id, estado=EstadoInscripcion.ACTIVO))
        insc_ctrl.inscribir_alumno(InscripcionCreate(estudiante_id=alumno3.id, catedra_academica_id=guitarra.id, periodo_id=periodo.id, estado=EstadoInscripcion.ACTIVO))
        insc_ctrl.inscribir_alumno(InscripcionCreate(estudiante_id=alumno4.id, catedra_academica_id=guitarra.id, periodo_id=periodo.id, estado=EstadoInscripcion.ACTIVO))
        insc_ctrl.inscribir_alumno(InscripcionCreate(estudiante_id=alumno5.id, catedra_academica_id=guitarra.id, periodo_id=periodo.id, estado=EstadoInscripcion.ACTIVO))
        insc_ctrl.inscribir_alumno(InscripcionCreate(estudiante_id=alumno6.id, catedra_academica_id=guitarra.id, periodo_id=periodo.id, estado=EstadoInscripcion.ACTIVO))
        insc_ctrl.inscribir_alumno(InscripcionCreate(estudiante_id=alumno7.id, catedra_academica_id=guitarra.id, periodo_id=periodo.id, estado=EstadoInscripcion.ACTIVO))

        # 🏁 Calificaciones
        calif_ctrl.registrar_calificacion(CalificacionCreate(estudiante_id=alumno.id, catedra_academica_id=guitarra.id, periodo_id=periodo.id, calificacion=Calificacion.AVANZADO, observaciones="Buen desempeño en clase."))
        calif_ctrl.registrar_calificacion(CalificacionCreate(estudiante_id=alumno2.id, catedra_academica_id=guitarra.id, periodo_id=periodo.id, calificacion=Calificacion.CONSOLIDADO, observaciones="Necesita mejorar en las prácticas."))
        calif_ctrl.registrar_calificacion(CalificacionCreate(estudiante_id=alumno3.id, catedra_academica_id=guitarra.id, periodo_id=periodo.id, calificacion=Calificacion.EN_PROCESO, observaciones="Excelente participación en clase."))
        calif_ctrl.registrar_calificacion(CalificacionCreate(estudiante_id=alumno4.id, catedra_academica_id=guitarra.id, periodo_id=periodo.id, calificacion=Calificacion.EN_PROCESO, observaciones="Excelente participación en clase."))
        calif_ctrl.registrar_calificacion(CalificacionCreate(estudiante_id=alumno5.id, catedra_academica_id=guitarra.id, periodo_id=periodo.id, calificacion=Calificacion.EN_PROCESO, observaciones="Excelente participación en clase."))
        calif_ctrl.registrar_calificacion(CalificacionCreate(estudiante_id=alumno6.id, catedra_academica_id=guitarra.id, periodo_id=periodo.id, calificacion=Calificacion.EN_PROCESO, observaciones="Excelente participación en clase."))
        calif_ctrl.registrar_calificacion(CalificacionCreate(estudiante_id=alumno7.id, catedra_academica_id=guitarra.id, periodo_id=periodo.id, calificacion=Calificacion.EN_PROCESO, observaciones="Excelente participación en clase."))

        return True

    except Exception as e:
        current_app.logger.error(f"Error al generar el seed académico: {e}", exc_info=True)
        return None
