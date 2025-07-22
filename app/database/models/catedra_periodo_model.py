from typing import Dict
from app.database.db_config import db

class CatedraAcademica(db.Model):
    """Modelo para las cátedras por período académico"""

    __tablename__ = 'catedra_academica'

    id = db.Column(db.Integer, primary_key=True)
    profesor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    catedra = db.Column(db.String(50))  # Se puede validar con Enum Catedra
    periodo_id = db.Column(db.Integer, db.ForeignKey("periodo_academico.id"))
    grupo = db.Column(db.String(10))  # Ejemplo: "A", "B", etc.
    cupos = db.Column(db.Integer, default=20)

    # Relaciones
    profesor = db.relationship('Usuario', back_populates='catedras_academicas')
    periodo = db.relationship('PeriodoAcademico', back_populates='catedras')
    inscripciones = db.relationship(
        'Inscripcion',
        back_populates='catedra_academica',
        lazy='dynamic'
    )


    def __repr__(self) -> str:
        return f'<CatedraAcademica profesor_id={self.profesor_id} catedra={self.catedra}>'
    
    def to_dict(self) -> Dict[str, any]:
        return {
            'id': self.id,
            'profesor_id': self.profesor_id,
            'catedra': self.catedra,
            'periodo_id': self.periodo_id,
            'grupo': self.grupo,
            'cupos': self.cupos
        }