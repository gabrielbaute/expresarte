from typing import List, Tuple
from enum import Enum

class Lenguaje(Enum):
    """Enum para la cátedra de Lenguaje"""

    LENGUAJE_INICIAL = "Lenguaje Inicial"
    LENGUAJE_INTERMEDIO = "Lenguaje intermedio"
    LENGUAJE_I = "Lenguaje I"
    LENGUAJE_II = "Lenguaje II"

    def __repr__(self):
        return f"{self.value}"
    
    def __str__(self) -> str:
        return f"{self.value}"

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(e.value, e.name.replace("_", " ").title()) for e in cls]