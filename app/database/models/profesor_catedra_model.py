from typing import Dict
from app.database.db_config import db

class ProfesorCatedra(db.Model):
    """Modelo para las cátedras asignadas a un profesor"""
    __tablename__ = 'profesor_catedra'
    id = db.Column(db.Integer, primary_key=True)
    profesor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    instrumento = db.Column(db.String(50))
    
    # Relaciones
    profesor = db.relationship('Usuario', back_populates='catedras')

    def __repr__(self):
        return f'<ProfesorCatedra profesor_id={self.profesor_id} instrumento={self.instrumento}>'

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'profesor_id': self.profesor_id,
            'instrumento': self.instrumento
        }