from typing import List, Tuple
from enum import Enum

class Instrumento(Enum):
    """Enum para la cátedra de instrumentos"""

    BAJO = "Bajo"
    BATERIA = "Batería"
    CANTO = "Canto"
    CUATRO = "Cuatro"
    GUITARRA = "Guitarra"
    GUITARRA_ELECTRICA = "Guitarra Eléctrica"
    PERCUSION_MENOR = "Percusión Menor"
    TECLADO = "Teclado"
    VIOLIN = "Violín"

    def __repr__(self):
        return f"{self.value}"
    
    def __str__(self) -> str:
        return f"{self.value}"

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(e.value, e.name.replace("_", " ").title()) for e in cls]
    
    @classmethod
    def to_list(cls) -> List[str]:
        """Devuelve una lista con los valores de cada instrumento"""
        return [role.value for role in cls]