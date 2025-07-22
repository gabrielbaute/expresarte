from typing import Optional
from flask import current_app

from app.database.controllers import UserController
from app.config.settings import Config


def create_initial_super_admin() -> Optional[bool]:
    """Crea el usuario super_admin al iniciar la aplicación por primera vez."""
    admin_nombre = Config.ADMIN_NOMBRE
    admin_apellido = Config.ADMIN_APELLIDO or "Admin"
    admin_email = Config.ADMIN_EMAIL
    admin_password = Config.ADMIN_PASSWORD

    try:
        # Verificar que las credenciales están configuradas
        if not all([admin_nombre, admin_apellido, admin_email, admin_password]):
            print("Credenciales de admin no configuradas en las variables de entorno")
            return False

        # Crear controller (sin current_user ya que es el primer usuario)
        controller = UserController()
        
        # Verifica si ya existen usuarios con rango super_admin en la aplicación
        existing_super_admins = controller.get_users_by_role("super_admin", only_active=False)
        if existing_super_admins:
            print(f"Ya existen {len(existing_super_admins)} super admins en el sistema")
            return True

        # Crear el super admin
        super_admin = controller.create_user(
            primer_nombre=admin_nombre,
            primer_apellido=admin_apellido,
            email=admin_email,
            password=admin_password,
            role="super_admin",
            sexo="N/A",
            activo=True
        )

        if super_admin:
            print(
                f"Super admin creado exitosamente: "
                f"Nombre: {admin_nombre}, Email: {admin_email}"
            )
            return True

    except Exception as e:
        current_app.logger.error(f"Error al crear el super admin: {str(e)}", exc_info=True)
        return False