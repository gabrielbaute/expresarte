from flask import current_app
from werkzeug.security import generate_password_hash
from datetime import datetime
from typing import Optional, List

from app.database.db_config import db
from app.database.models import Usuario
from app.database.enums import Role, Permission
from app.database.controllers.db_controller import DatabaseController

class UserController(DatabaseController):
    def __init__(self, current_user: Optional[Usuario] = None):
        super().__init__()
        self.current_user = current_user
    
    # Métodos internos de validación
    def _validate_role(self, role: str) -> Role:
        """Valida que el rol exista en el sistema."""
        try:
            return Role(role)
        except Exception as e:
            valid_roles = [r.value for r in Role]
            current_app.logger.error(f"Rol inválido: {role}. Roles válidos: {valid_roles}")
    
    def _check_permission(self, permission: Permission) -> bool:
        """Verifica si el usuario actual tiene un permiso."""
        try:
            if self.current_user and not self.current_user.has_permission(permission):
                current_app.logger.error(f"Se requiere permiso: {permission.name}")
                return False
            return True
        except Exception as e:
            current_app.logger.error(f"Error al verificar permisos: {e}")
            return None

    # Métodos para obtener un usuario
    def get_user_by_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por email."""
        if not self._check_permission(Permission.VIEW_USERS):
            return None
        else:
            try:
                user = Usuario.query.filter_by(email=email).first()
                return user
            except Exception as e:
                current_app.logger.error(f"Error al obtener usuario por email: {e}")
                return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Usuario]:
        """Obtiene un usuario por ID."""
        if not self._check_permission(Permission.VIEW_USERS):
            return None
        else:
            try:
                user = Usuario.query.get(user_id)
                return user
            except Exception as e:
                current_app.logger.error(f"Error al obtener usuario por ID: {e}")
                return None

    def get_users_by_role(self, role: str, only_active: bool = True) -> List[Usuario]:
        """
        Obtiene todos los usuarios con un rol específico.
        
        Args:
            role: Rol a filtrar (debe ser uno de los Role values)
            only_active: Si True, solo devuelve usuarios activos
        
        Returns:
            List[Usuario]: Lista de usuarios con el rol especificado
        
        Raises:
            InvalidRoleError: Si el rol no es válido
        """
        self._check_permission(Permission.VIEW_USERS)
        self._validate_role(role)  # Esto lanza InvalidRoleError si el rol no es válido
        
        query = Usuario.query.filter_by(role=role)
        if only_active:
            query = query.filter_by(activo=True)
            
        return query.all()
    
    # Métodos para crear y actualizar usuarios
    def create_user(
        self,
        primer_nombre: str,
        primer_apellido: str,
        email: str,
        password: str,
        role: str,
        segundo_nombre: Optional[str] = None,
        segundo_apellido: Optional[str] = None,
        cedula: Optional[str] = None,
        fecha_nacimiento: Optional[datetime] = None,
        sexo: Optional[str] = None,
        activo: bool = True
    ) -> Optional[Usuario]:
        """
        Crea un nuevo usuario con validación de roles y permisos.
        
        Args:
            primer_nombre: Primer nombre del usuario
            segundo_nombre: Segundo nombre del usuario
            primer_apellido: Primer apellido del usuario
            segundo_apellido: Segundo apellido del usuario
            email: Email único
            password: Contraseña en texto plano
            role: Rol del usuario (debe ser uno de los Role values)
            cedula: Opcional para menores
            fecha_nacimiento: Opcional
            sexo: Opcional (para agrupaciones vocales)
            activo: Si el usuario está activo
        
        Returns:
            Usuario: El objeto de usuario creado
        
        Raises:
            InvalidRoleError: Si el rol no es válido
            EmailAlreadyExistsError: Si el email ya existe
            PermissionDeniedError: Si no tiene permisos para crear usuarios
        """
        if not self._check_permission(Permission.CREATE_USERS):
            return None

        valid_role = self._validate_role(role)
        if not valid_role:
            current_app.logger.error("Creación abortada: rol inválido.")
            return None

        if Usuario.query.filter_by(email=email).first():
            current_app.logger.error(f"No se puede crear usuario: email {email} ya está en uso.")
            return None

        user = Usuario(
            primer_nombre=primer_nombre,
            segundo_nombre=segundo_nombre,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
            cedula=cedula,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            activo=activo
        )

        db.session.add(user)
        if self._commit_or_rollback() is True:
            return user

        current_app.logger.error("Falló el commit al crear usuario.")
        return None
    
    def update_user(
        self,
        user_id: int,
        **kwargs
    ) -> Optional[Usuario]:
        """Actualiza campos específicos de un usuario"""
        
        if not self._check_permission(Permission.EDIT_USERS):
            return None

        user = self.get_user_by_id(user_id)
        if not user:
            current_app.logger.error(f"No se puede actualizar: usuario con ID {user_id} no encontrado.")
            return None

        # Validar el rol si se está actualizando
        if 'role' in kwargs:
            if not self._validate_role(kwargs['role']):
                current_app.logger.error("Actualización abortada: rol inválido.")
                return None

        # Campos editables
        for key, value in kwargs.items():
            if hasattr(user, key) and key != 'id':
                setattr(user, key, value)

        if self._commit_or_rollback() is True:
            return user

        current_app.logger.error("Falló el commit al actualizar usuario.")
        return None

    
    def deactivate_user(self, user_id: int) -> bool:
        """
        Desactiva un usuario (borrado lógico).
        
        Args:
            user_id: ID del usuario a desactivar
        
        Returns:
            bool: True si se desactivó correctamente
        
        Raises:
            UserNotFoundError: Si el usuario no existe
            PermissionDeniedError: Si no tiene permisos
        """
        self._check_permission(Permission.DELETE_USERS)
        user = self.get_user_by_id(user_id)
        
        if not user:
            current_app.logger.error(f"Usuario con ID {user_id} no encontrado")
        
        user.activo = False
        return self._commit_or_rollback() is True
    
    # Métodos misceláneos
    def count_users_by_role(self, role: str, only_active: bool = True) -> int:
        """
        Cuenta los usuarios con un rol específico.
        
        Args:
            role: Rol a filtrar
            only_active: Si True, solo cuenta usuarios activos
        
        Returns:
            int: Número de usuarios con el rol especificado
        """
        self._check_permission(Permission.VIEW_USERS)
        self._validate_role(role)
        
        query = Usuario.query.filter_by(role=role)
        if only_active:
            query = query.filter_by(activo=True)
            
        return query.count()

    def get_all_teachers(self, only_active: bool = True) -> List[Usuario]:
        """Obtiene todos los usuarios con rol de profesor"""
        return self.get_users_by_role(Role.TEACHER.value, only_active)

    def get_all_students(self, only_active: bool = True) -> List[Usuario]:
        """Obtiene todos los usuarios con rol de estudiante"""
        return self.get_users_by_role(Role.STUDENT.value, only_active)

    def get_all_admins(self, only_active: bool = True) -> List[Usuario]:
        """Obtiene todos los usuarios con rol de admin o super_admin"""
        admins = self.get_users_by_role(Role.ADMIN.value, only_active)
        super_admins = self.get_users_by_role(Role.SUPER_ADMIN.value, only_active)
        return admins + super_admins