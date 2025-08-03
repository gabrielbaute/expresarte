from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.server.forms import CreateUserForm, UserStatusForm, AsignarCatedraForm, ActualizarUserForm
from app.schemas import UserCreate, UserUpdate, ProfesorCatedraCreate, ProfesorCatedraUpdate
from app.controllers import ControllerFactory
from app.database.enums import Catedra, Role

controller = ControllerFactory(current_user=current_user)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

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
