from typing import Dict
from app.database.db_config import db
from app.database.enums import Catedra

class ProfesorCatedra(db.Model):
    """Modelo para las cátedras asignadas a un profesor"""
    __tablename__ = 'profesor_catedra'
    id = db.Column(db.Integer, primary_key=True)
    profesor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    catedra = db.Column(db.Enum(Catedra), nullable=False)
    
    # Relaciones
    profesor = db.relationship('Usuario', back_populates='catedras')

    def __repr__(self):
        return f'<ProfesorCatedra profesor_id={self.profesor_id} catedra={self.catedra}>'

    @property
    def tipo(self):
        return self.catedra.tipo

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'profesor_id': self.profesor_id,
            'catedra': self.catedra
        }