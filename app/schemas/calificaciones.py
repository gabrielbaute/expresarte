from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.database.enums import Calificacion

class CalificacionCreate(BaseModel):
    estudiante_id: int
    catedra_academica_id: int
    periodo_id: int
    calificacion: Calificacion
    observaciones: Optional[str] = None
    fecha_calificacion: datetime = datetime.now()

class CalificacionUpdate(BaseModel):
    estudiante_id: Optional[int] = None
    catedra_academica_id: Optional[int] = None
    periodo_id: Optional[int] = None
    calificacion: Optional[Calificacion] = None
    observaciones: Optional[str] = None
    fecha_calificacion: Optional[datetime] = None

class CalificacionResponse(BaseModel):
    id: int
    estudiante_id: int
    catedra_academica_id: int
    periodo_id: int
    calificacion: Calificacion
    observaciones: Optional[str] = None
    fecha_calificacion: datetime

    model_config = {
        "from_attributes": True
    }