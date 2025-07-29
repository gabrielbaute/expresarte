from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.database.enums import EstadoInscripcion

class InscripcionCreate(BaseModel):
    estudiante_id: int
    catedra_academica_id: int
    estado: EstadoInscripcion = EstadoInscripcion.PENDIENTE
    fecha_inscripcion: datetime = datetime.now()

class InscripcionUpdate(BaseModel):
    estudiante_id: Optional[int] = None
    catedra_academica_id: Optional[int] = None
    estado: Optional[EstadoInscripcion] = None
    fecha_inscripcion: Optional[datetime] = None

class InscripcionResponse(BaseModel):
    id: int
    estudiante_id: int
    catedra_academica_id: int
    periodo_id: int
    estado: EstadoInscripcion
    fecha_inscripcion: datetime

    model_config = {
        "from_attributes": True
    }