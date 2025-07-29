from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PeriodoAcademicoCreate(BaseModel):
    nombre: str
    fecha_inicio: datetime
    fecha_fin: datetime
    activo: bool = True

class PeriodoAcademicoUpdate(BaseModel):
    nombre: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    activo: Optional[bool] = None

class PeriodoAcademicoResponse(BaseModel):
    id: int
    nombre: str
    fecha_inicio: datetime
    fecha_fin: datetime
    activo: bool

    model_config = {
        "from_attributes": True
    }