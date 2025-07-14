from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from app.server.forms import LoginForm
from app.database.controllers import UserController
from app.database.models import Usuario

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        controller = UserController()  # No necesitas current_user para login
        user = controller.get_user_by_email(email)

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash(f"Bienvenido, {user.primer_nombre} 👋", "success")
            return redirect(url_for('main.index'))
        else:
            flash("Correo o contraseña incorrectos.", "danger")

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for('auth.login'))
