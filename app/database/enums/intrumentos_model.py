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
    
    def __str__(self):
        return f"{self.value}"