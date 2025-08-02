from typing import Dict
from app.database.db_config import db
from app.database.enums import Calificacion


class Calificacion(db.Model):
    """Modelo para las calificaciones de los alumnos"""
    
    __tablename__ = 'calificacion'

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    catedra_academica_id = db.Column(db.Integer, db.ForeignKey("catedra_academica.id"))
    periodo_id = db.Column(db.Integer, db.ForeignKey("periodo_academico.id"))
    calificacion = db.Column(db.Enum(Calificacion), nullable=True)
    observaciones = db.Column(db.Text)
    fecha = db.Column(db.DateTime)

    def __repr__(self) -> str:
        return f'<Evaluacion alumno_id={self.estudiante_id} catedra_academica_id={self.catedra_academica_id}>'
    
    # Relaciones
    periodo = db.relationship("PeriodoAcademico")
    alumno = db.relationship('Usuario', back_populates='calificaciones')
    catedra_academica = db.relationship('CatedraAcademica', back_populates='calificaciones')
    
    def to_dict(self) -> Dict[str, any]:
        return {
            'id': self.id,
            'alumno_id': self.estudiante_id,
            'catedra_academica_id': self.catedra_academica_id,
            'calificacion': self.calificacion.value if self.calificacion else None,
            'observaciones': self.observaciones,
            'fecha': self.fecha
        }