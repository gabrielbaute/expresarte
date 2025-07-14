from enum import Enum

class Lenguaje(Enum):
    """Enum para la cátedra de Lenguaje"""

    LENGUAJE_INICIAL = "Lenguaje Inicial"
    LENGUAJE_INTERMEDIO = "Lenguaje intermedio"
    LENGUAJE_I = "Lenguaje I"
    LENGUAJE_II = "Lenguaje II"

    def __repr__(self):
        return f"{self.value}"
    
    def __str__(self):
        return f"{self.value}"