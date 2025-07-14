from enum import Enum

class Sexo(Enum):
    """Enum para las tablas de sexo de los usuarios"""

    MASCULINO = "M"
    FEMENINO = "F"
    NO_APLICA = "N/A"

    def __repr__(self):
        return f"{self.value}"
    
    def __str__(self) -> str:
        return f"{self.value}"

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(e.value, e.name.replace("_", " ").title()) for e in cls]