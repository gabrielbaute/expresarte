from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_migrate import Migrate

login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def init_login_manager(app):
    """Función que inicializa la extensión LoginManager."""
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, inicie sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from app.database.controllers import UserController
        controller = UserController()
        return controller.get_user_by_id(user_id)


    return login_manager

def init_migrate(app, db):
    """Función que inicializa la extensión Migrate."""
    migrate.init_app(app, db)

def init_csrf(app):
    """Función que inicializa la extensión CSRFProtect."""
    app.config['WTF_CSRF_ENABLED'] = True
    csrf.init_app(app)