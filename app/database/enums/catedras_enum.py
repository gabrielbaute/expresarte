from enum import Enum
from typing import List, Tuple

class Catedra(Enum):
    BAJO = ("Bajo", "instrumento")
    BATERIA = ("Batería", "instrumento")
    CANTO = ("Canto", "instrumento")
    CUATRO = ("Cuatro", "instrumento")
    GUITARRA = ("Guitarra", "instrumento")
    GUITARRA_ELECTRICA = ("Guitarra Eléctrica", "instrumento")
    PERCUSION_MENOR = ("Percusión Menor", "instrumento")
    TECLADO = ("Teclado", "instrumento")
    VIOLIN = ("Violín", "instrumento")

    LENGUAJE_INICIAL = ("Lenguaje Inicial", "lenguaje")
    LENGUAJE_INTERMEDIO = ("Lenguaje Intermedio", "lenguaje")
    LENGUAJE_I = ("Lenguaje I", "lenguaje")
    LENGUAJE_II = ("Lenguaje II", "lenguaje")

    def __init__(self, label: str, tipo: str):
        self._label = label
        self._tipo = tipo

    def __str__(self) -> str:
        return self.name

    @property
    def label(self) -> str:
        return self._label

    @property
    def tipo(self) -> str:
        return self._tipo

    @property
    def value(self):
        return self.name

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(e.value, e.name.replace("_", " ").title()) for e in cls]

    @classmethod
    def to_list(cls) -> List[str]:
        return [e.value for e in cls]

    @classmethod
    def from_label(cls, label: str) -> "Catedra":
        for item in cls:
            if item.value == label:
                return item
        raise ValueError(f"{label} no es una cátedra válida")


    def to_dict(self) -> dict:
        return {
            "label": self._label,
            "tipo": self._tipo
        }