from typing import Dict
from app.database.db_config import db
from datetime import datetime

class Inscripcion(db.Model):
    """Modelo para las inscripciones de los alumnos"""
    
    __tablename__ = 'inscripcion'

    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    catedra_academica_id = db.Column(db.Integer, db.ForeignKey("catedra_academica.id"))
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default="activo")  # "activo", "retirado", "aprobado"

    def __repr__(self) -> str:
        return f'<Inscripcion alumno_id={self.alumno_id} catedra_academica_id={self.catedra_academica_id}>'
    
    def to_dict(self) -> Dict[str, any]:
        return {
            'id': self.id,
            'alumno_id': self.alumno_id,
            'catedra_academica_id': self.catedra_academica_id,
            'fecha_inscripcion': self.fecha_inscripcion,
            'estado': self.estado
        }