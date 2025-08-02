from typing import List, Tuple
from enum import Enum

class Sexo(str, Enum):
    """Enum para las tablas de sexo de los usuarios"""

    MASCULINO = "M"
    FEMENINO = "F"
    NO_APLICA = "N/A"

    def __repr__(self):
        return f"{self.value}"
    
    def __str__(self) -> str:
        return f"{self.value}"

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(e.value, e.name.replace("_", " ").title()) for e in cls]

    @classmethod
    def to_list(cls) -> List[str]:
        """Devuelve una lista con los valores de cada sexo"""
        return [role.value for role in cls]