from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.server.forms import LoginForm
from app.controllers import ControllerFactory
from app.server.forms import RequestResetPasswordForm, PasswordResetForm
from app.mail import ExpresarteMailer, MailTokenHandler

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        controller = ControllerFactory().get_user_controller()
        user = controller.get_user_model_by_email(email)
        
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

@auth_bp.route('/request-reset-password', methods=['GET', 'POST'])
def request_reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        controller = ControllerFactory().get_user_controller()
        try:
            user = controller.get_user_by_email(email)
            mailer = ExpresarteMailer(current_app)
            mailer.send_reset_password(email, user.id)
        except Exception:
            pass  # No revelamos si el correo existe

        flash("Si el correo está registrado, recibirás instrucciones para restablecer tu contraseña.", "info")
        return redirect(url_for('auth.login'))

    return render_template('auth/request_reset_password.html', form=form)

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user_id = MailTokenHandler.decode_token(token)
    if not user_id:
        flash("El enlace ha expirado o es inválido.", "danger")
        return redirect(url_for('auth.request_reset_password'))

    form = PasswordResetForm()
    if form.validate_on_submit():
        new_password = form.new_password.data
        controller = ControllerFactory().get_user_controller()
        controller.update_user_password(user_id, new_password)
        flash("Tu contraseña ha sido actualizada correctamente.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)
