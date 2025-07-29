from pydantic import BaseModel
from typing import Optional

class ProfesorCatedraCreate(BaseModel):
    profesor_id: int
    catedra: str

class ProfesorCatedraUpdate(BaseModel):
    profesor_id: Optional[int] = None
    catedra: Optional[str] = None

class ProfesorCatedraResponse(BaseModel):
    id: int
    profesor_id: int
    catedra: str

    model_config = {
        "from_attributes": True
    }