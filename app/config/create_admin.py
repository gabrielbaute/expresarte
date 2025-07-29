from typing import Optional
from flask import current_app
from app.controllers import ControllerFactory
from app.config.settings import Config
from app.database.enums import Role, Sexo

def create_initial_super_admin() -> Optional[bool]:
    """Crea el usuario super_admin al iniciar la aplicación por primera vez."""
    admin_nombre = Config.ADMIN_NOMBRE
    admin_apellido = Config.ADMIN_APELLIDO or "Admin"
    admin_email = Config.ADMIN_EMAIL
    admin_password = Config.ADMIN_PASSWORD

    try:
        if not all([admin_nombre, admin_apellido, admin_email, admin_password]):
            current_app.logger.warning("Credenciales de admin no configuradas en las variables de entorno")
            return False

        # Crear controller sin usuario actual (es el primer admin del sistema)
        controller = ControllerFactory(current_user=None).get_user_controller()

        # Verifica si ya existen usuarios con el rol super_admin
        existing_super_admins = controller.get_users_by_role(Role.SUPER_ADMIN, only_active=False)
        if existing_super_admins:
            current_app.logger.info(f"Ya existen {len(existing_super_admins)} super admins en el sistema")
            return True

        # Crear el super admin
        super_admin = controller.create_user(
            primer_nombre=admin_nombre,
            primer_apellido=admin_apellido,
            email=admin_email,
            password=admin_password,
            role=Role.SUPER_ADMIN,
            sexo=Sexo.NO_APLICA,
            activo=True
        )

        if not super_admin:
            current_app.logger.warning("No se pudo crear el usuario super admin por motivos desconocidos")
            return False

        current_app.logger.info(
            f"Super admin creado exitosamente: Nombre: {admin_nombre}, Email: {admin_email}"
        )
        return True

    except Exception as e:
        current_app.logger.error(f"Error al crear el super admin: {str(e)}", exc_info=True)
        return False
