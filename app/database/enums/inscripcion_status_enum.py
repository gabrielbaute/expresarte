from typing import List, Tuple
from enum import Enum

class EstadoInscripcion(str, Enum):
    """Enum para los estados de inscripción"""

    ACTIVO = "activo"
    RETIRADO = "retirado"
    APROBADO = "aprobado"
    INACTIVO = "inactivo"
    PENDIENTE = "pendiente"
    CANCELADO = "cancelado"
    ESPERANDO_CONFIRMACION = "esperando_confirmacion"
    RECHAZADO = "rechazado"
    ESPERANDO_PAGO = "esperando_pago"

    def __repr__(self):
        return f"{self.value}"
    
    def __str__(self) -> str:
        return f"{self.value}"

    @classmethod
    def choices(cls) -> List[Tuple[str, bool]]:
        return [(e.value, e.name.replace("_", " ").title()) for e in cls]