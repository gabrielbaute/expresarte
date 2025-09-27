from typing import Optional, List, Union
from flask import current_app
from werkzeug.security import generate_password_hash

from app.schemas import UserCreate, UserUpdate, UserResponse
from app.database.models import Usuario
from app.database.enums import Role, Permission
from app.errors import NotFoundError, InvalidRoleError, PermissionDeniedError
from app.controllers.db_controller import DatabaseController

class UserController(DatabaseController):
    def __init__(self, db, current_user=None):
        super().__init__(db)
        self.current_user = current_user

    # Validaciones internas
    def _validate_role(self, role: Union[str, Role]) -> str:
        """Valida el rol de un usuario y si ese rol existe.
        
        Args:
            role (Union[str, Role]): Rol del usuario.
        
        Returns:
            str: Rol del usuario.
        
        Raises:
            InvalidRoleError: Si el rol no es válido.
        """
        role_str = role.value if isinstance(role, Role) else role
        if role_str not in Role.to_list():
            raise InvalidRoleError(role_str, Role.to_list())
        return role_str

    def _check_permission(self, permission: Permission) -> None:
        """Verifica si un usuario tiene permiso para realizar una acción.
        
        Args:
            permission (Permission): Permiso a verificar.
        
        Raises:
            PermissionDeniedError: Si el usuario no tiene el permiso requerido.
        """
        if self.current_user is None:
            if permission == Permission.VIEW_USERS:
                return  # permite vista sin autenticación solo para este caso
            raise PermissionDeniedError("No hay usuario autenticado")

        if not self.current_user.has_permission(permission):
            raise PermissionDeniedError(
                f"El usuario '{self.current_user.email}' no tiene el permiso requerido: '{permission.name}'"
            )

    # Métodos CRUD para usuarios
    def create_user(self, data: UserCreate) -> UserResponse:
        """Crea un usuario nuevo
        
        Args:
            data (UserCreate): Datos del usuario.
        
        Returns:
            UserResponse: El usuario creado.
        
        Raises:
            PermissionDeniedError: Si ya existe un usuario con el mismo correo.
        """
        if self.session.query(Usuario).filter_by(email=data.email).first():
            raise PermissionDeniedError("Ya existe un usuario con ese correo.")

        role = self._validate_role(data.role)
        hashed_pwd = generate_password_hash(data.password_hash)

        user = Usuario(
            email=data.email,
            password_hash=hashed_pwd,
            primer_nombre=data.primer_nombre,
            segundo_nombre=data.segundo_nombre,
            primer_apellido=data.primer_apellido,
            segundo_apellido=data.segundo_apellido,
            sexo=data.sexo,
            fecha_nacimiento=data.fecha_nacimiento,
            cedula=data.cedula,
            role=role
        )
        self.session.add(user)
        self._commit_or_rollback()
        return self._to_response(user, UserResponse)

    def edit_user(self, user_id: int, data: UserUpdate) -> UserResponse:
        """Edita los detalles de un usuario por su ID.
        
        Args:
            user_id (int): ID del usuario.
            data (UserUpdate): Datos actualizados del usuario.
        
        Returns:
            UserResponse: El usuario actualizado.
        """
        user = self._get_or_fail(Usuario, user_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        self._commit_or_rollback()
        return self._to_response(user, UserResponse)

    def list_users(self, role: Optional[str] = None) -> List[UserResponse]:
        """Lista todos los usuarios.
        
        Args:
            role (Optional[str]): Filtra por rol si se proporciona.
        
        Returns:
            List[UserResponse]: Lista de usuarios.
        """
        self._check_permission(Permission.VIEW_USERS)
        query = self.session.query(Usuario)
        if role:
            query = query.filter_by(role=role)
        return self._bulk_to_response(query.all(), UserResponse)

    def disable_user(self, user_id: int) -> UserResponse:
        """Desactiva un usuario por su ID.
        
        Args:
            user_id (int): ID del usuario.
        
        Returns:
            UserResponse: El usuario desactivado.
        """
        user = self._get_or_fail(Usuario, user_id)
        user.activo = False
        self._commit_or_rollback()
        return self._to_response(user, UserResponse)

    # Métodos misceláneos
    def count_users_by_role(self, role: str, only_active: bool = True) -> int:
        """Cuenta el número de usuarios por rol.
        
        Args:
            role (str): Rol del usuario.
            only_active (bool): Si True, solo cuenta los usuarios activos.
        
        Returns:
            int: Número de usuarios.
        """
        self._check_permission(Permission.VIEW_USERS)
        self._validate_role(role)

        query = self.session.query(Usuario).filter_by(role=role)
        if only_active:
            query = query.filter_by(activo=True)

        return query.count()

    def get_user_by_email(self, email: str) -> UserResponse:
        """Obtiene un usuario por su correo electrónico.
        
        Args:
            email (str): Correo electrónico del usuario.
        
        Returns:
            UserResponse: El usuario encontrado.
        """
        self._check_permission(Permission.VIEW_USERS)
        user = self.session.query(Usuario).filter_by(email=email).first()
        return self._to_response(user, UserResponse)

    def get_user_by_id(self, user_id: int) -> UserResponse:
        """Obtiene un usuario por su ID.
        
        Args:
            user_id (int): ID del usuario.
        
        Returns:
            UserResponse: El usuario encontrado.
        """
        self._check_permission(Permission.VIEW_USERS)
        user = self.session.get(Usuario, user_id)
        return self._to_response(user, UserResponse)

    def get_users_by_role(self, role: Union[str, Role], only_active: bool = True) -> List[UserResponse]:
        """Obtiene todos los usuarios por rol.
        
        Args:
            role (Union[str, Role]): Rol del usuario.
            only_active (bool): Si True, solo devuelve los usuarios activos.
        
        Returns:
            List[UserResponse]: Lista de usuarios.
        """
        self._check_permission(Permission.VIEW_USERS)

        query = self.session.query(Usuario)

        if isinstance(role, Role):
            query = query.filter_by(role=role.value)
        elif isinstance(role, str):
            if role != "all":
                if role not in Role.to_list():
                    raise InvalidRoleError(role, Role.to_list())
                query = query.filter_by(role=role)
            # Si es "all", no se filtra el rol

        if only_active:
            query = query.filter_by(activo=True)

        return self._bulk_to_response(query.all(), UserResponse)

    def get_all_teachers(self, only_active: bool = True) -> List[UserResponse]:
        """Obtiene todos los profesores.
        
        Args:
            only_active (bool): Si True, solo devuelve los profesores activos.
        
        Returns:
            List[UserResponse]: Lista de profesores.
        """
        return self.get_users_by_role(Role.TEACHER.value, only_active)

    def get_all_students(self, only_active: bool = True) -> List[UserResponse]:
        """Obtiene todos los estudiantes.
        
        Args:
            only_active (bool): Si True, solo devuelve los estudiantes activos.
        
        Returns:
            List[UserResponse]: Lista de estudiantes.
        """
        return self.get_users_by_role(Role.STUDENT.value, only_active)

    def get_all_admins(self, only_active: bool = True) -> List[UserResponse]:
        """Obtiene todos los administradores.
        
        Args:
            only_active (bool): Si True, solo devuelve los administradores activos.
        
        Returns:
            List[UserResponse]: Lista de administradores.
        """
        return self.get_users_by_role(Role.ADMIN.value, only_active)

    def get_user_model_by_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un modelo de usuario por su correo electrónico.
        
        Args:
            email (str): Correo electrónico del usuario.
        
        Returns:
            Optional[Usuario]: El modelo de usuario encontrado, si existe.
        """
        return self.session.query(Usuario).filter_by(email=email).first()

    def update_user_password(self, user_id: int, new_password: str) -> bool:
        """Actualiza la contraseña de un usuario.
        
        Args:
            user_id (int): ID del usuario.
            new_password (str): Nueva contraseña.
        
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        user = self._get_or_fail(Usuario, user_id)
        user.password_hash = generate_password_hash(new_password)
        self._commit_or_rollback()
        return True