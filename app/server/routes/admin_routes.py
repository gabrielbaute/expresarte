from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.server.forms import CreateUserForm, UserStatusForm
from app.database.controllers import UserController
from app.database.models import Usuario

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/usuarios/crear', methods=['GET', 'POST'])
@login_required
def crear_usuario():
    if not current_user.is_admin():
        flash("Acceso denegado: solo administradores pueden crear usuarios.", "danger")
        return redirect(url_for('main.index'))

    form = CreateUserForm()
    if form.validate_on_submit():
        user_ctrl = UserController(current_user=current_user)
        nuevo_usuario = user_ctrl.create_user(
            primer_nombre=form.primer_nombre.data,
            segundo_nombre=form.segundo_nombre.data,
            primer_apellido=form.primer_apellido.data,
            segundo_apellido=form.segundo_apellido.data,
            email=form.email.data,
            password=form.password.data,
            role=form.role.data,
            cedula=form.cedula.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            sexo=form.sexo.data,
            # activo=form.activo.data
        )

        if nuevo_usuario:
            flash(f"Usuario {nuevo_usuario.email} creado con éxito 🎉", "success")
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

    user_ctrl = UserController(current_user=current_user)
    usuarios = user_ctrl.get_users_by_role(role='all', only_active=False)

    return render_template('admin/list_users.html', usuarios=usuarios, form=form)

@admin_bp.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    if not current_user.is_admin():
        flash("Acceso denegado: solo administradores pueden editar usuarios.", "danger")
        return redirect(url_for('main.index'))

    user_ctrl = UserController(current_user=current_user)
    usuario = user_ctrl.get_user_by_id(id)

    if not usuario:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('admin.lista_usuarios'))

    form = CreateUserForm(obj=usuario)

    if form.validate_on_submit():
        updated = user_ctrl.update_user(
            user_id=id,
            primer_nombre=form.primer_nombre.data,
            segundo_nombre=form.segundo_nombre.data,
            primer_apellido=form.primer_apellido.data,
            segundo_apellido=form.segundo_apellido.data,
            email=form.email.data,
            role=form.role.data,
            cedula=form.cedula.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            sexo=form.sexo.data
            # Nota: no actualizamos contraseña desde esta vista por seguridad
        )

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
        user_ctrl = UserController(current_user=current_user)
        actualizado = user_ctrl.update_user(user_id=id, activo=form.activo.data)

        if actualizado:
            flash(f"Estado actualizado para {actualizado.email}.", "success")
        else:
            flash("No se pudo modificar el estado del usuario.", "danger")
    else:
        flash("Formulario inválido.", "danger")

    return redirect(url_for('admin.lista_usuarios'))
