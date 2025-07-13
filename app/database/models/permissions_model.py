"""
Sistema de permisos para los roles de usuario.
"""
from enum import Enum, auto

class Permission(Enum):
    """
    Enumeración que define todos los permisos posibles en el sistema.
    Cada permiso es único y se autogenera con auto().
    """
    # Permisos de gestión de usuarios
    CREATE_USERS = auto()
    EDIT_USERS = auto()
    DELETE_USERS = auto()
    VIEW_USERS = auto()
    
    # Permisos de gestión académica
    CREATE_COURSES = auto()
    EDIT_COURSES = auto()
    DELETE_COURSES = auto()
    VIEW_COURSES = auto()
    
    # Permisos de canciones/proyectos
    CREATE_SONGS = auto()
    EDIT_SONGS = auto()
    DELETE_SONGS = auto()
    ASSIGN_SONGS = auto()
    VIEW_SONGS = auto()
    
    # Permisos de evaluación
    EDIT_GRADES = auto()
    VIEW_GRADES = auto()
    
    # Permisos administrativos
    MANAGE_ACADEMIC_PERIODS = auto()
    GENERATE_REPORTS = auto()