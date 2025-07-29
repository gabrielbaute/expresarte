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
    def _validate_role(self, role: str) -> str:
        if role not in Role.to_list():
            raise InvalidRoleError(role, Role.to_list())
        return role

    def _check_permission(self, permission: Permission) -> None:
        if self.current_user is None:
            raise PermissionDeniedError("No hay usuario autenticado")

        if permission not in self.current_user.permissions:
            raise PermissionDeniedError(
                f"El usuario '{self.current_user.email}' no tiene el permiso requerido: '{permission.name}'"
            )

    # Métodos CRUD para usuarios
    def create_user(self, data: UserCreate) -> UserResponse:
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
        user = self._get_or_fail(Usuario, user_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        self._commit_or_rollback()
        return self._to_response(user, UserResponse)


    def list_users(self, role: Optional[str] = None) -> List[UserResponse]:
        query = self.session.query(Usuario)
        if role:
            query = query.filter_by(role=role)
        return self._bulk_to_response(query.all(), UserResponse)

    def disable_user(self, user_id: int) -> UserResponse:
        user = self._get_or_fail(Usuario, user_id)
        user.activo = False
        self._commit_or_rollback()
        return self._to_response(user, UserResponse)

    # Métodos misceláneos
    def count_users_by_role(self, role: str, only_active: bool = True) -> int:
        """Cuenta el número de usuarios por rol."""
        self._check_permission(Permission.VIEW_USERS)
        self._validate_role(role)

        query = self.session.query(Usuario).filter_by(role=role)
        if only_active:
            query = query.filter_by(activo=True)

        return query.count()

    def get_user_by_email(self, email: str) -> UserResponse:
        """Obtiene un usuario por su correo electrónico."""
        self._check_permission(Permission.VIEW_USERS)
        user = self.session.query(Usuario).filter_by(email=email).first()
        return self._to_response(user, UserResponse)

    def get_user_by_id(self, user_id: int) -> UserResponse:
        self._check_permission(Permission.VIEW_USERS)
        user = self.session.get(Usuario, user_id)
        return self._to_response(user, UserResponse)

    def get_users_by_role(self, role: Union[str, Role], only_active: bool = True) -> List[UserResponse]:
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
        return self.get_users_by_role(Role.TEACHER.value, only_active)

    def get_all_students(self, only_active: bool = True) -> List[UserResponse]:
        return self.get_users_by_role(Role.STUDENT.value, only_active)

    def get_all_admins(self, only_active: bool = True) -> List[UserResponse]:
        return self.get_users_by_role(Role.ADMIN.value, only_active)

