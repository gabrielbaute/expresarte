from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.database.enums import Catedra

class CatedraAcademicaCreate(BaseModel):
    profesor_id: int
    catedra: Catedra
    periodo_id: int
    grupo: Optional[str] = None
    cupos: Optional[int] = 20

class CatedraAcademicaUpdate(BaseModel):
    profesor_id: Optional[int] = None
    catedra: Optional[Catedra] = None
    periodo_id: Optional[int] = None
    grupo: Optional[str] = None
    cupos: Optional[int] = 20

class CatedraAcademicaResponse(BaseModel):
    id: int
    profesor_id: int
    catedra: Catedra
    periodo_id: int
    grupo: Optional[str] = None
    cupos: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    model_config = {
        "from_attributes": True
    }