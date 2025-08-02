from typing import Dict
from app.database.db_config import db
from datetime import datetime
from app.database.enums import EstadoInscripcion

class Inscripcion(db.Model):
    """Modelo para las inscripciones de los alumnos"""
    
    __tablename__ = 'inscripcion'

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    catedra_academica_id = db.Column(db.Integer, db.ForeignKey("catedra_academica.id"))
    periodo_id = db.Column(db.Integer, db.ForeignKey("periodo_academico.id"))
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.Enum(EstadoInscripcion), default="activo")

    # Relaciones
    student = db.relationship('Usuario', back_populates='inscripciones')
    catedra_academica = db.relationship('CatedraAcademica', back_populates='inscripciones')
    periodo = db.relationship("PeriodoAcademico", back_populates="inscripciones")

    def __repr__(self) -> str:
        return f'<Inscripcion estudiante_id={self.estudiante_id} catedra_academica_id={self.catedra_academica_id}>'
    
    def to_dict(self) -> Dict[str, any]:
        return {
            'id': self.id,
            'estudiante_id': self.estudiante_id,
            'catedra_academica_id': self.catedra_academica_id,
            'fecha_inscripcion': self.fecha_inscripcion,
            'estado': self.estado
        }

    @property
    def esta_activa(self) -> bool:
        return self.estado == "activo"

    @property
    def esta_retirada(self) -> bool:
        return self.estado == "retirado"

    @property
    def esta_aprobada(self) -> bool:
        return self.estado == "aprobado"
