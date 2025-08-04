from datetime import datetime
from flask import(Blueprint, redirect, url_for, render_template, flash, request, abort)
from flask_login import login_required, current_user

from app.controllers import ControllerFactory
from app.server.forms import CalificacionForm, SetCalificacionForm
from app.database.models import Usuario, CatedraAcademica, Calificacion, PeriodoAcademico
from app.database.enums import Catedra
from app.schemas import CalificacionCreate, CalificacionUpdate

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teachers', template_folder='templates')

# Rutas de la navegación de la app
@teacher_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_teacher():
        flash("Acceso denegado.", "danger")
        return redirect(url_for('main.index'))

    # Cátedras asignadas
    controller = ControllerFactory(current_user=current_user)
    catedra_ctrl = controller.get_profesor_catedra_controller()
    catedras = catedra_ctrl.get_catedras_by_profesor(current_user.id)
    
    fecha_actual = datetime.now().strftime('%d/%m/%Y')
    hora_actual = datetime.now().strftime('%H:%M')

    return render_template('teachers/teacher_dashboard.html', 
        profesor=current_user,
        catedras=catedras,
        fecha_actual=fecha_actual,
        hora_actual=hora_actual
    )

@teacher_bp.route('/catedra/<nombre>/estudiantes')
@login_required
def ver_estudiantes(nombre):
    if not current_user.is_teacher():
        flash("Acceso denegado.", "danger")
        return redirect(url_for('main.index'))

    try:
        catedra_enum = Catedra.from_label(nombre)
    except ValueError:
        flash("Cátedra no válida.", "warning")
        return redirect(url_for('teacher.dashboard'))

    factory = ControllerFactory(current_user=current_user)
    catedra_ctrl = factory.get_profesor_catedra_controller()
    periodo_ctrl = factory.get_periodo_academico_controller()
    calif_ctrl = factory.get_calificacion_controller()

    periodo = periodo_ctrl.get_active_periodo()
    if not periodo:
        flash("No hay período académico activo.", "warning")
        return redirect(url_for('teacher.dashboard'))

    catedra_academica = catedra_ctrl.get_catedra_academica(
        current_user.id, catedra_enum, periodo.id
    )
    if not catedra_academica:
        flash("No se encontró la cátedra en este período.", "warning")
        return redirect(url_for('teacher.dashboard'))

    estudiantes = catedra_ctrl.get_students_by_catedra(current_user.id, catedra_enum)

    resumen = []
    for estudiante in estudiantes:
        calificacion = calif_ctrl.obtener_calificacion(estudiante.id, catedra_academica.id)
        resumen.append({
            "id": estudiante.id,
            "nombre": f"{estudiante.primer_nombre} {estudiante.primer_apellido}",
            "calificacion": calificacion.calificacion if calificacion else "Sin registrar",
            "observaciones": calificacion.observaciones if calificacion else ""
        })
    form = SetCalificacionForm()
    return render_template('teachers/ver_estudiantes.html',
        estudiantes=resumen,
        nombre_catedra=catedra_enum.label,
        catedra_id=catedra_academica.id,
        periodo_id=periodo.id,
        form=form,
    )

@teacher_bp.route('/calificacion/<int:alumno_id>/<int:catedra_id>/<int:periodo_id>/editar', methods=['POST'])
@login_required
def editar_calificacion(alumno_id, catedra_id, periodo_id):
    form = SetCalificacionForm()
    if form.validate_on_submit():
        factory = ControllerFactory(current_user=current_user)
        calif_ctrl = factory.get_calificacion_controller()

        calificacion = calif_ctrl.obtener_calificacion(alumno_id, catedra_id)

        if calificacion:
            # Ya existe: actualizar
            update_data = CalificacionUpdate(calificacion=form.nota.data)
            calif_ctrl.editar_calificacion(calificacion.id, update_data)
        else:
            # No existe: registrar
            data = CalificacionCreate(
                estudiante_id=alumno_id,
                catedra_academica_id=catedra_id,
                periodo_id=periodo_id,
                calificacion=form.nota.data,
                observaciones=""
            )
            calif_ctrl.registrar_calificacion(data)

        flash("Calificación actualizada exitosamente.", "success")
    else:
        flash("Error al actualizar la calificación.", "danger")

    return redirect(url_for('teacher.ver_estudiantes', nombre=Catedra.label))


@teacher_bp.route("/asignar-calificaciones/<int:catedra_id>", methods=["GET", "POST"])
@login_required
def asignar_calificaciones(catedra_id):
    catedra = CatedraAcademica.query.get_or_404(catedra_id)
    if catedra.profesor_id != current_user.id:
        abort(403)

    controller = ControllerFactory().get_calificacion_controller()
    inscripciones = catedra.inscripciones.filter_by(estado="activo").all()
    
    # Crear lista de formularios, uno por estudiante
    formset = []
    for inscripcion in inscripciones:
        form = CalificacionForm()
        form.alumno_id.data = inscripcion.student.id
        existente = controller.obtener_calificacion(inscripcion.student, catedra)
        if existente:
            form.nota_final.data = existente.nota
        formset.append((inscripcion.student, form))

    if request.method == "POST":
        exitos = 0
        for estudiante, form in formset:
            form.process(request.form)
            if form.validate():
                nota = form.nota_final.data
                resultado = controller.registrar_nota(
                    alumno=estudiante,
                    catedra=catedra,
                    nota=nota
                )
                if resultado:
                    exitos += 1
        flash(f"{exitos} nota(s) registradas exitosamente.", "success")
        return redirect(url_for("teacher.ver_estudiantes", nombre=catedra.catedra))

    return render_template("teachers/asignar_calificaciones.html",
        formset=formset,
        catedra=catedra,
        form=form
    )