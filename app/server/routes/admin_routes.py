from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.server.forms import(
    CreateUserForm, 
    UserStatusForm, 
    AsignarCatedraForm, 
    ActualizarUserForm, 
    PeriodoAcademicoForm, 
    CrearPeriodoAcademicoForm,
    CatedraPeriodoForm
)
from app.schemas import (
    UserCreate,
    UserUpdate, 
    ProfesorCatedraCreate, 
    ProfesorCatedraUpdate, 
    PeriodoAcademicoCreate, 
    PeriodoAcademicoUpdate,
    CatedraAcademicaCreate
)
from app.controllers import ControllerFactory
from app.database.enums import Catedra, Role
from app.database.models import PeriodoAcademico

controller = ControllerFactory(current_user=current_user)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Gestión de Períodos Usuarios

@admin_bp.route('/usuarios/crear', methods=['GET', 'POST'])
@login_required
def crear_usuario():
    if not current_user.is_admin():
        flash("Acceso denegado: solo administradores pueden crear usuarios.", "danger")
        return redirect(url_for('main.index'))

    form = CreateUserForm()
    if form.validate_on_submit():
        from werkzeug.security import generate_password_hash

        nuevo_usuario = UserCreate(
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            primer_nombre=form.primer_nombre.data,
            segundo_nombre=form.segundo_nombre.data or None,
            primer_apellido=form.primer_apellido.data,
            segundo_apellido=form.segundo_apellido.data or None,
            role=form.role.data,
            sexo=form.sexo.data,
            cedula=form.cedula.data or None,
            fecha_nacimiento=form.fecha_nacimiento.data
        )
        user_ctrl = controller.get_user_controller()
        resultado = user_ctrl.create_user(nuevo_usuario)

        if resultado:
            flash(f"Usuario {resultado.email} creado con éxito 🎉", "success")
            return redirect(url_for('main.index'))
        else:
            flash("Hubo un problema al crear el usuario.", "danger")

    return render_template('admin/create_user.html', form=form)

@admin_bp.route('/usuarios')
@login_required
def lista_usuarios():
    form = UserStatusForm()
    if not current_user.is_admin():
        flash("Acceso denegado: solo administradores pueden ver esta página.", "danger")
        return redirect(url_for('main.index'))

    user_ctrl = controller.get_user_controller()
    usuarios = user_ctrl.get_users_by_role(role='all', only_active=False)

    return render_template('admin/list_users.html', usuarios=usuarios, form=form)

@admin_bp.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    if not current_user.is_admin():
        flash("Acceso denegado: solo administradores pueden editar usuarios.", "danger")
        return redirect(url_for('main.index'))

    user_ctrl = ControllerFactory(current_user=current_user).get_user_controller()
    usuario = user_ctrl.get_user_by_id(id)

    if not usuario:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('admin.lista_usuarios'))

    form = ActualizarUserForm(obj=usuario)

    if form.validate_on_submit():
        user_update_data = UserUpdate(
            primer_nombre=form.primer_nombre.data,
            segundo_nombre=form.segundo_nombre.data,
            primer_apellido=form.primer_apellido.data,
            segundo_apellido=form.segundo_apellido.data,
            email=form.email.data,
            role=form.role.data,
            cedula=form.cedula.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            sexo=form.sexo.data
        )

        updated = user_ctrl.edit_user(user_id=id, data=user_update_data)

        if updated:
            flash("Usuario actualizado correctamente.", "success")
            return redirect(url_for('admin.lista_usuarios'))
        else:
            flash("Hubo un problema al actualizar el usuario.", "danger")

    return render_template('admin/edit_user.html', form=form, usuario=usuario)

@admin_bp.route('/usuarios/<int:id>/estado', methods=['POST'])
@login_required
def cambiar_estado_usuario(id):
    if not current_user.is_admin():
        flash("Acceso denegado: solo administradores pueden modificar estado de usuarios.", "danger")
        return redirect(url_for('main.index'))

    form = UserStatusForm()
    if form.validate_on_submit():
        user_ctrl = controller.get_user_controller()
        updated = user_ctrl.edit_user(user_id=id, data=UserUpdate(activo=form.activo.data))

        if updated:
            flash(f"Estado actualizado para {updated.email}.", "success")
        else:
            flash("No se pudo modificar el estado del usuario.", "danger")
    else:
        flash("Formulario inválido.", "danger")

    return redirect(url_for('admin.lista_usuarios'))

# Gestión de Profesores

@admin_bp.route('/profesores')
@login_required
def lista_profesores():
    if not current_user.is_admin():
        flash("Acceso denegado.", "danger")
        return redirect(url_for('main.index'))

    user_ctrl = controller.get_user_controller()
    catedra_ctrl = controller.get_profesor_catedra_controller()

    profesores = user_ctrl.get_all_teachers(only_active=True)
    listado = []

    for profe in profesores:
        listado.append({
            "obj": profe,
            "catedras": catedra_ctrl.get_catedras_by_profesor(profe.id)
        })

    return render_template('admin/list_profesores.html', profesores=listado)

@admin_bp.route('/profesores/<int:id>/asignar-catedra', methods=['GET', 'POST'])
@login_required
def asignar_catedra(id):
    if not current_user.is_admin():
        flash("Acceso denegado.", "danger")
        return redirect(url_for('main.index'))

    user_ctrl = controller.get_user_controller()
    catedra_ctrl = controller.get_profesor_catedra_controller()
    profesor = user_ctrl.get_user_by_id(id)

    if not profesor or not profesor.role == Role.TEACHER:
        flash("Profesor inválido.", "warning")
        return redirect(url_for('admin.lista_profesores'))

    form = AsignarCatedraForm()
    if form.validate_on_submit():
        catedra = Catedra.from_label(form.catedra.data)
        resultado = catedra_ctrl.asignar_catedra(ProfesorCatedraCreate(profesor_id=profesor.id, catedra=catedra))

        if resultado:
            flash(f"Cátedra {catedra.value} asignada a {profesor.primer_nombre}.", "success")
        else:
            flash("No se pudo asignar la cátedra.", "danger")
        return redirect(url_for('admin.lista_profesores'))

    return render_template('admin/asignar_catedra.html', form=form, profesor=profesor)

@admin_bp.route('/profesores/<int:profesor_id>/remover-catedra/<nombre_catedra>', methods=['POST'])
@login_required
def remover_catedra(profesor_id, nombre_catedra):
    if not current_user.is_admin():
        flash("Acceso denegado.", "danger")
        return redirect(url_for('main.index'))

    user_ctrl = controller.get_user_controller()
    profesor = user_ctrl.get_user_by_id(profesor_id)

    if not profesor or not profesor.role == Role.TEACHER:
        flash("Profesor inválido.", "warning")
        return redirect(url_for('admin.lista_profesores'))

    catedra_ctrl = controller.get_profesor_catedra_controller()

    try:
        catedra_enum = Catedra.from_label(nombre_catedra)
    except ValueError:
        flash("Cátedra inválida.", "danger")
        return redirect(url_for('admin.lista_profesores'))

    resultado = catedra_ctrl.eliminar_asignacion(profesor.id, catedra_enum)
    if resultado:
        flash(f"Cátedra '{nombre_catedra}' removida de {profesor.primer_nombre}.", "info")
    else:
        flash("No se pudo remover la cátedra.", "warning")

    return redirect(url_for('admin.lista_profesores'))

# Gestión de Períodos Académicos

@admin_bp.route('/periodos-academicos', methods=['GET', 'POST'])
@login_required
def gestionar_periodos():
    if not current_user.is_admin():
        flash("Acceso denegado.", "danger")
        return redirect(url_for('main.index'))

    periodo_ctrl = ControllerFactory(current_user=current_user).get_periodo_academico_controller()

    form = PeriodoAcademicoForm()
    if form.validate_on_submit():
        data = PeriodoAcademicoCreate(
            nombre=form.nombre.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_fin=form.fecha_fin.data,
            activo=form.activo.data
        )
        try:
            periodo_ctrl.crear_periodo(data)
            flash("Período académico creado exitosamente.", "success")
        except Exception as e:
            flash(str(e.orig), "danger")
        return redirect(url_for('admin.gestionar_periodos'))

    periodos = periodo_ctrl.listar_periodos()
    return render_template(
        'admin/periodos_academicos.html',
        form=form,
        periodos=periodos
    )

@admin_bp.route('/periodos-academicos/crear', methods=['GET', 'POST'])
@login_required
def crear_periodo():
    if not current_user.is_admin():
        flash("Acceso denegado.", "danger")
        return redirect(url_for('main.index'))

    periodo_ctrl = ControllerFactory(current_user=current_user).get_periodo_academico_controller()
    form = CrearPeriodoAcademicoForm()

    if form.validate_on_submit():
        data = PeriodoAcademicoCreate(
            nombre=form.nombre.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_fin=form.fecha_fin.data,
            activo=form.activo.data
        )
        try:
            periodo_ctrl.crear_periodo(data)
            flash("Período académico creado exitosamente.", "success")
            return redirect(url_for('admin.gestionar_periodos'))
        except Exception as e:
            flash(str(e), "danger")

    return render_template('admin/crear_periodo.html', form=form)

@admin_bp.route('/periodos-academicos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_periodo(id):
    if not current_user.is_admin():
        flash("Acceso denegado.", "danger")
        return redirect(url_for('main.index'))

    factory = ControllerFactory(current_user=current_user)
    periodo_ctrl = factory.get_periodo_academico_controller()
    catedra_ctrl = factory.get_catedra_academica_controller()
    user_ctrl = factory.get_user_controller()

    periodo = periodo_ctrl._get_or_fail(PeriodoAcademico, id)
    form = PeriodoAcademicoForm(obj=periodo)
    catedra_form = CatedraPeriodoForm()

    # Cargar opciones del enum Catedra y lista de profesores
    catedra_form.catedra.choices = Catedra.choices()
    profesores = user_ctrl.get_all_teachers()
    catedra_form.profesor_id.choices = [(0, "— Sin profesor —")] + [(p.id, p.primer_nombre) for p in profesores]

    # Edición del período
    if form.validate_on_submit() and not catedra_form.submit.data:
        data = PeriodoAcademicoUpdate(
            nombre=form.nombre.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_fin=form.fecha_fin.data,
            activo=form.activo.data
        )
        try:
            periodo_ctrl.update_periodo(periodo_id=id, data=data)
            flash("Período actualizado correctamente.", "success")
        except Exception as e:
            flash(f"Error al actualizar: {str(e)}", "danger")
        return redirect(url_for('admin.editar_periodo', id=id))

    # Asignación de cátedra académica
    if catedra_form.validate_on_submit() and catedra_form.submit.data:
        profesor = catedra_form.profesor_id.data if catedra_form.profesor_id.data != 0 else None
        nueva_catedra = CatedraAcademicaCreate(
            periodo_id=id,
            catedra=catedra_form.catedra.data,
            grupo=catedra_form.grupo.data,
            profesor_id=profesor
        )
        try:
            catedra_ctrl.crear_catedra(nueva_catedra)
            flash("Cátedra asignada correctamente.", "success")
        except Exception as e:
            flash(f"Error al asignar cátedra: {str(e)}", "danger")
        return redirect(url_for('admin.editar_periodo', id=id))

    # Listar cátedras ya asignadas
    catedras = catedra_ctrl.listar_por_periodo(id)

    return render_template("admin/editar_periodo.html", form=form, catedra_form=catedra_form,
                           periodo=periodo, catedras=catedras)

@admin_bp.route('/periodos-academicos/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_periodo(id):
    if not current_user.is_admin():
        flash("Acceso denegado.", "danger")
        return redirect(url_for('main.index'))

    periodo_ctrl = ControllerFactory(current_user=current_user).get_periodo_academico_controller()
    try:
        periodo_ctrl.delete_periodo(id)
        flash("Período académico eliminado.", "success")
    except Exception as e:
        flash(f"No se pudo eliminar el período: {str(e)}", "danger")

    return redirect(url_for('admin.gestionar_periodos'))

@admin_bp.route('/periodos-academicos/<int:id>/activar', methods=['POST'])
@login_required
def activar_periodo(id):
    if not current_user.is_admin():
        flash("Acceso denegado.", "danger")
        return redirect(url_for('main.index'))

    periodo_ctrl = ControllerFactory(current_user=current_user).get_periodo_academico_controller()
    periodo_ctrl.activar_periodo(id)
    flash("Período académico activado.", "success")
    return redirect(url_for('admin.gestionar_periodos'))

@admin_bp.route('/periodos-academicos/<int:id>/desactivar', methods=['POST'])
@login_required
def desactivar_periodo(id):
    if not current_user.is_admin():
        flash("Acceso denegado.", "danger")
        return redirect(url_for('main.index'))

    periodo_ctrl = ControllerFactory(current_user=current_user).get_periodo_academico_controller()
    periodo_ctrl.desactivar_periodo(id)
    flash("Período académico desactivado.", "warning")
    return redirect(url_for('admin.gestionar_periodos'))

@admin_bp.route('/periodos-academicos/<int:id>/ver', methods=['GET'])
@login_required
def ver_periodo(id):
    if not current_user.is_admin():
        flash("Acceso denegado.", "danger")
        return redirect(url_for('main.index'))

    factory = ControllerFactory(current_user=current_user)
    periodo_ctrl = factory.get_periodo_academico_controller()
    catedra_ctrl = factory.get_catedra_academica_controller()
    inscripcion_ctrl = factory.get_inscripcion_controller()
    user_ctrl = factory.get_user_controller()

    periodo = periodo_ctrl._get_or_fail(PeriodoAcademico, id)
    catedras = catedra_ctrl.listar_por_periodo(periodo.id)

    resumen = []
    for cat in catedras:
        profesor = user_ctrl.get_user_by_id(cat.profesor_id) if cat.profesor_id else None
        inscritos = inscripcion_ctrl.contar_estudiantes_en_catedra(cat.id) or 0  # ← asegúrate que devuelva int

        resumen.append({
            "nombre": cat.catedra.label,
            "grupo": cat.grupo,
            "profesor": f"{profesor.primer_nombre} {profesor.primer_apellido}" if profesor else "Sin asignar",
            "inscritos": inscritos
        })

    return render_template("admin/ver_periodo.html", periodo=periodo, resumen=resumen)
