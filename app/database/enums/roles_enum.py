from typing import List, Tuple
from enum import Enum

class Role(str, Enum):
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
    def choices(cls) -> List[Tuple[str, str]]:
        """Devuelve una lista de tuplas de los roles y sus valores."""
        return [(e.value, e.name.replace("_", " ").title()) for e in cls]

    @classmethod
    def to_list(cls) -> List[str]:
        """Devuelve una lista con los valores de cada rol"""
        return [role.value for role in cls]