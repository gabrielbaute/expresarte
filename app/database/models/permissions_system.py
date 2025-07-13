from typing import Set, Dict

from app.database.models.roles_model import Role
from app.database.models.permissions_model import Permission

# Mapeo de jerarquía de roles (números más bajos = mayor privilegio)
ROLE_HIERARCHY: Dict[Role, int] = {
    Role.SUPER_ADMIN: 1,
    Role.ADMIN: 2,
    Role.ACADEMIC: 3,
    Role.TEACHER: 4,
    Role.STUDENT: 5
}

# Mapeo de permisos por rol
ROLE_PERMISSIONS: Dict[Role, Set[Permission]] = {
    Role.SUPER_ADMIN: {perm for perm in Permission},  # Todos los permisos
    Role.ADMIN: {
        Permission.CREATE_USERS,
        Permission.EDIT_USERS,
        Permission.VIEW_USERS,
        Permission.CREATE_COURSES,
        Permission.EDIT_COURSES,
        Permission.VIEW_COURSES,
        Permission.CREATE_SONGS,
        Permission.EDIT_SONGS,
        Permission.VIEW_SONGS,
        Permission.ASSIGN_SONGS,
        Permission.EDIT_GRADES,
        Permission.VIEW_GRADES,
        Permission.MANAGE_ACADEMIC_PERIODS,
        Permission.GENERATE_REPORTS
    },
    Role.ACADEMIC: {
        Permission.VIEW_USERS,
        Permission.CREATE_COURSES,
        Permission.EDIT_COURSES,
        Permission.VIEW_COURSES,
        Permission.CREATE_SONGS,
        Permission.EDIT_SONGS,
        Permission.VIEW_SONGS,
        Permission.ASSIGN_SONGS,
        Permission.EDIT_GRADES,
        Permission.VIEW_GRADES
    },
    Role.TEACHER: {
        Permission.VIEW_COURSES,
        Permission.VIEW_SONGS,
        Permission.EDIT_GRADES,
        Permission.VIEW_GRADES
    },
    Role.STUDENT: {
        Permission.VIEW_COURSES,
        Permission.VIEW_SONGS,
        Permission.VIEW_GRADES
    }
}

def user_has_permission(user_role: Role, required_permission: Permission) -> bool:
    """
    Verifica si un rol de usuario tiene un permiso específico,
    considerando la jerarquía de roles.
    
    Args:
        user_role: Rol del usuario (miembro de la enumeración Role)
        required_permission: Permiso a verificar (miembro de Permission)
    
    Returns:
        bool: True si el usuario tiene el permiso, False en caso contrario
    
    Example:
        >>> user_has_permission(Role.TEACHER, Permission.EDIT_GRADES)
        True
        >>> user_has_permission(Role.STUDENT, Permission.EDIT_GRADES)
        False
    """
    # Verificar si el rol tiene directamente el permiso
    if required_permission in ROLE_PERMISSIONS.get(user_role, set()):
        return True
    
    # Verificar si algún rol superior tiene el permiso
    user_level = ROLE_HIERARCHY.get(user_role, float('inf'))
    for role, level in ROLE_HIERARCHY.items():
        if level < user_level and required_permission in ROLE_PERMISSIONS.get(role, set()):
            return True
    
    return False