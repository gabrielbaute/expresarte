from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from app.database.enums import Sexo, Role

class UserCreate(BaseModel):
    email: EmailStr
    password_hash: str
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    sexo: Sexo
    cedula: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    role: Role

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password_hash: Optional[str] = None
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    sexo: Optional[Sexo] = None
    cedula: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    activo: Optional[bool] = None
    role: Optional[Role] = None

class UserLogin(BaseModel):
    email: EmailStr
    password_hash: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    sexo: Sexo
    cedula: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    activo: bool
    role: Role
    fecha_creacion: datetime

    model_config = {
        "from_attributes": True
    }