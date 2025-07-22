from typing import Dict
from app.database.db_config import db


class Calificacion(db.Model):
    """Modelo para las calificaciones de los alumnos"""
    
    __tablename__ = 'calificacion'

    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    catedra_academica_id = db.Column(db.Integer, db.ForeignKey("catedra_academica.id"))
    nota = db.Column(db.Float)
    observaciones = db.Column(db.Text)
    fecha = db.Column(db.DateTime)

    def __repr__(self) -> str:
        return f'<Evaluacion alumno_id={self.alumno_id} catedra_academica_id={self.catedra_academica_id}>'
    
    # Relaciones
    alumno = db.relationship('Usuario', back_populates='calificaciones')
    catedra_academica = db.relationship('CatedraAcademica', back_populates='calificaciones')
    
    def to_dict(self) -> Dict[str, any]:
        return {
            'id': self.id,
            'alumno_id': self.alumno_id,
            'catedra_academica_id': self.catedra_academica_id,
            'nota': self.nota,
            'observaciones': self.observaciones,
            'fecha': self.fecha
        }

    @property
    def es_aprobado(self) -> bool:
        return self.nota is not None and self.nota >= 10