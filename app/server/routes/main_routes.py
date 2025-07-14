from flask import(
    Blueprint,
    redirect,
    url_for,
    render_template,
    flash,
)

main_bp = Blueprint('main', __name__, template_folder='templates')

# Rutas de la navegación de la app
@main_bp.route('/')
def index():
    return render_template('main/index.html')