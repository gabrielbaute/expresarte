from enum import Enum

class Sexo(Enum):
    """Enum para las tablas de sexo de los usuarios"""

    MASCULINO = "M"
    FEMENINO = "F"
    NO_APLICA = "N/A"

    def __repr__(self):
        return f"{self.value}"
    
    def __str__(self):
        return f"{self.value}"