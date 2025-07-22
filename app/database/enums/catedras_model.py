# app/database/enums/catedras_model.py

from enum import Enum
from typing import List, Tuple

class Catedra(Enum):
    # Instrumentos
    BAJO = "Bajo"
    BATERIA = "Batería"
    CANTO = "Canto"
    CUATRO = "Cuatro"
    GUITARRA = "Guitarra"
    GUITARRA_ELECTRICA = "Guitarra Eléctrica"
    PERCUSION_MENOR = "Percusión Menor"
    TECLADO = "Teclado"
    VIOLIN = "Violín"

    # Lenguaje musical
    LENGUAJE_INICIAL = "Lenguaje Inicial"
    LENGUAJE_INTERMEDIO = "Lenguaje Intermedio"
    LENGUAJE_I = "Lenguaje I"
    LENGUAJE_II = "Lenguaje II"

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(e.value, e.name.replace("_", " ").title()) for e in cls]

    @classmethod
    def to_list(cls) -> List[str]:
        return [e.value for e in cls]

    def tipo(self) -> str:
        if "Lenguaje" in self.value:
            return "lenguaje"
        return "instrumento"