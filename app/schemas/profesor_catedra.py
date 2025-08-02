from pydantic import BaseModel, field_serializer
from typing import Optional
from app.database.enums import Catedra

class ProfesorCatedraCreate(BaseModel):
    profesor_id: int
    catedra: str

class ProfesorCatedraUpdate(BaseModel):
    profesor_id: Optional[int] = None
    catedra: Optional[str] = None

class ProfesorCatedraResponse(BaseModel):
    id: int
    profesor_id: int
    catedra: Catedra
    tipo: str

    @field_serializer("catedra")
    def serialize_catedra(self, v: Catedra, _info):
        return v.label  # ← retorna el nombre “Guitarra” en lugar de “GUITARRA”

    @field_serializer("tipo")
    def serialize_tipo(self, v: Catedra, _info):
        return v.tipo # ← retorna el tipo “instrumento” o “lenguaje”

    model_config = {
        "from_attributes": True
    }