from typing import List, Tuple
from enum import Enum

class Calificacion(Enum):
    """Enum para las calificaciones de los alumnos"""
    
    EN_PROCESO = "en_proceso"
    AVANZADO = "avanzado"
    CONSOLIDADO = "consolidado"

    def __repr__(self):
        return f"{self.value}"
    
    def __str__(self) -> str:
        return f"{self.value}"

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(e.value, e.name) for e in cls]

    @classmethod
    def to_list(cls) -> List[str]:
        return [e.value for e in cls]