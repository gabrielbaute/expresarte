from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.server.forms import CreateUserForm
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
