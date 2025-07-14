"""
Sistema de permisos para los roles de usuario.
"""
from enum import Enum

class Role(Enum):
    """
    Enumeración que define los roles disponibles en el sistema.
    Los valores son strings legibles que se almacenarán en la DB.
    """
    SUPER_ADMIN = 'super_admin'
    ADMIN = 'admin'
    ACADEMIC = 'academic'
    TEACHER = 'teacher'
    STUDENT = 'student'

    def __repr__(self):
        return f"{self.value}"
    
    def __str__(self) -> str:
        return f"{self.value}"

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(e.value, e.name.replace("_", " ").title()) for e in cls]