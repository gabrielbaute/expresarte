from datetime import datetime
from flask import(Blueprint, redirect, url_for, render_template, flash, request, abort)
from flask_login import login_required, current_user

from app.database.controllers import ProfesorCatedraController, CalificacionController
from app.server.forms import CalificacionForm
from app.database.models import Usuario, CatedraAcademica, Calificacion, PeriodoAcademico
from app.database.enums import Catedra

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teachers', template_folder='templates')

# Rutas de la navegación de la app
@teacher_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_teacher():
        flash("Acceso denegado.", "danger")
        return redirect(url_for('main.index'))

    # Cátedras asignadas
    catedra_ctrl = ProfesorCatedraController()
    catedras = catedra_ctrl.get_catedra_by_profesor(current_user)

    fecha_actual = datetime.now().strftime('%d/%m/%Y')

    return render_template('teachers/teacher_dashboard.html', 
        profesor=current_user,
        catedras=catedras,
        fecha_actual=fecha_actual
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

    # Obtener el período activo
    periodo = PeriodoAcademico.query.filter_by(activo=True).first()
    if not periodo:
        flash("No hay período académico activo.", "warning")
        return redirect(url_for('teacher.dashboard'))

    # Buscar la CatedraAcademica específica
    catedra_academica = CatedraAcademica.query.filter_by(
        profesor_id=current_user.id,
        catedra=catedra_enum.value,
        periodo_id=periodo.id
    ).first()

    if not catedra_academica:
        flash("No se encontró la cátedra en este período.", "warning")
        return redirect(url_for('teacher.dashboard'))

    catedra_ctrl = ProfesorCatedraController()
    estudiantes = catedra_ctrl.get_students_by_catedra(current_user, catedra_enum)

    return render_template('teachers/ver_estudiantes.html',
        estudiantes=estudiantes,
        nombre_catedra=catedra_enum.value,
        catedra_id=catedra_academica.id
    )


@teacher_bp.route("/asignar-calificaciones/<int:catedra_id>", methods=["GET", "POST"])
@login_required
def asignar_calificaciones(catedra_id):
    catedra = CatedraAcademica.query.get_or_404(catedra_id)
    if catedra.profesor_id != current_user.id:
        abort(403)

    controller = CalificacionController()
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