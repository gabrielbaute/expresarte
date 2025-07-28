from flask import(
    Blueprint,
    redirect,
    url_for,
    render_template,
    flash,
)
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__, template_folder='templates')

# Rutas de la navegación de la app
@main_bp.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('main/index.html')