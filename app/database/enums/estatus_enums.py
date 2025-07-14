from typing import List, Tuple
from enum import Enum

class Estatus(Enum):
    """Enum para estatus del usuario"""

    ACTIVO = True
    INACTIVO = False

    def __repr__(self):
        return f"{self.value}"
    
    def __str__(self) -> str:
        return f"{self.value}"

    @classmethod
    def choices(cls) -> List[Tuple[str, bool]]:
        return [(e.value, e.name.replace("_", " ").title()) for e in cls]