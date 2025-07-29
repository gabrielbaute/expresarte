
class AppError(Exception):
    """Base de excepciones de dominio."""
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

class InvalidRoleError(AppError):
    def __init__(self, role: str, valid_roles: list[str]):
        detail = f"Rol inválido: '{role}'. Roles válidos: {valid_roles}"
        super().__init__(detail, status_code=422)

class PermissionDeniedError(AppError):
    def __init__(self, permission: str = ""):
        detail = f"Permiso denegado: {permission}" if permission else "Permiso insuficiente"
        super().__init__(detail, status_code=403)

class NotFoundError(AppError):
    def __init__(self, resource: str = "Recurso"):
        detail = f"{resource} no encontrado"
        super().__init__(detail, status_code=404)