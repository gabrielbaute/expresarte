from typing import Dict
from app.database.db_config import db

class PeriodoAcademico(db.Model):
    """Modelo para los períodos académicos"""

    __tablename__ = 'periodo_academico'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))  # Ejemplo: "2025-I"
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    activo = db.Column(db.Boolean, default=True)

    # Relaciones
    catedras = db.relationship(
        'CatedraAcademica',
        back_populates='periodo',
        lazy='dynamic'
    )

    def __repr__(self) -> str:
        return f'<PeriodoAcademico {self.nombre}>'
    
    def to_dict(self) -> Dict[str, any]:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'activo': self.activo
        }