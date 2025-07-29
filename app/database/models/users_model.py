from flask_login import UserMixin
from datetime import datetime
from typing import Optional

from app.database.db_config import db
from app.database.enums.permissions_model import Permission
from app.database.enums.roles_model import Role
from app.database.enums.permissions_system import user_has_permission

class Usuario(db.Model, UserMixin):
    """Modelo para la tabla de usuarios en la db"""
    
    __tablename__ = 'usuarios'
    
    # Información de la cuenta
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Datos personales
    primer_nombre = db.Column(db.String(50), nullable=False)
    segundo_nombre = db.Column(db.String(50))
    primer_apellido = db.Column(db.String(50), nullable=False)
    segundo_apellido = db.Column(db.String(50))
    sexo = db.Column(db.String(10), nullable=False)
    cedula = db.Column(db.String(20))  # Opcional para menores
    fecha_nacimiento = db.Column(db.Date)
    
    # Información de control de la cuenta
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), nullable=False)
    
    # Relaciones
    catedras = db.relationship('ProfesorCatedra', back_populates='profesor', lazy='dynamic')
    catedras_academicas = db.relationship('CatedraAcademica', back_populates='profesor', lazy='dynamic')
    inscripciones = db.relationship('Inscripcion', back_populates='student', lazy='dynamic')
    calificaciones = db.relationship('Calificacion', back_populates='alumno', lazy='dynamic')

    # Métodos requeridos por Flask-Login
    def get_id(self):
        return str(self.id)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombres': f"{self.primer_nombre} {self.segundo_nombre}",
            'apellidos': f"{self.primer_apellido} {self.segundo_apellido}",
            'email': self.email,
            'cedula': self.cedula if self.cedula else "No cedulado",
            'sexo': self.sexo,
            'fecha_nacimiento': self.fecha_nacimiento,
            "fecha_creacion": self.fecha_creacion,
            "activo": self.activo,
            'role': self.role,
        }

    @property
    def is_active(self):
        return self.activo
    
    @property
    def edad(self):
        if self.fecha_nacimiento:
            today = datetime.today()
            age = today.year - self.fecha_nacimiento.year
            if today.month < self.fecha_nacimiento.month or (today.month == self.fecha_nacimiento.month and today.day < self.fecha_nacimiento.day):
                age -= 1
            return age
        return None

    @property
    def nombre_completo(self) -> str:
        nombres = f"{self.primer_nombre} {self.segundo_nombre}".strip()
        apellidos = f"{self.primer_apellido} {self.segundo_apellido}".strip()
        return f"{nombres} {apellidos}"

    # Métodos para verificación de roles y permisos
    def get_role(self) -> Optional[Role]:
        """Devuelve el objeto Role correspondiente al rol del usuario"""
        try:
            return Role(self.role)
        except ValueError:
            return None
    
    def has_permission(self, permission: Permission) -> bool:
        """
        Verifica si el usuario tiene un permiso específico.
        
        Args:
            permission: Permiso a verificar (miembro de Permission)
        
        Returns:
            bool: True si tiene el permiso, False si no
        """
        user_role = self.get_role()
        if user_role is None:
            return False
        return user_has_permission(user_role, permission)
    
    # Métodos de conveniencia para verificación de roles
    def is_super_admin(self) -> bool:
        return self.role == Role.SUPER_ADMIN.value
    
    def is_admin(self) -> bool:
        return self.role == Role.ADMIN.value or self.is_super_admin()
    
    def is_academic(self) -> bool:
        return self.role == Role.ACADEMIC.value or self.is_admin()
    
    def is_teacher(self) -> bool:
        return self.role == Role.TEACHER.value or self.is_academic()
    
    def is_student(self) -> bool:
        return self.role == Role.STUDENT.value
    
    # Métodos específicos para profesores
    def can_teach(self, instrumento: str) -> bool:
        """Verifica si el profesor puede enseñar un instrumento específico"""
        if not self.is_teacher():
            return False
            
        return self.catedras.filter_by(
            catedra=instrumento
        ).first() is not None