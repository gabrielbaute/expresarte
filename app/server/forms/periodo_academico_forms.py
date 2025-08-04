from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional

class PeriodoAcademicoForm(FlaskForm):
    """Formulario para gestionar períodos académicos"""
    
    nombre = StringField('Nombre del Período', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de Inicio', validators=[DataRequired()])
    fecha_fin = DateField('Fecha de Fin', validators=[DataRequired()])
    activo = BooleanField('Activo')
    
    submit = SubmitField('Guardar Período')

class CrearPeriodoAcademicoForm(FlaskForm):
    """Formulario para crear un nuevo período académico"""

    nombre = StringField("Nombre del Período", validators=[DataRequired(), Length(max=50)])
    fecha_inicio = DateField("Fecha de Inicio", format='%Y-%m-%d', validators=[DataRequired()])
    fecha_fin = DateField("Fecha de Fin", format='%Y-%m-%d', validators=[DataRequired()])
    activo = BooleanField("¿Activo?", default=True)
    
    submit = SubmitField("Crear Período")
    
class CatedraPeriodoForm(FlaskForm):
    """Formulario para asignar una cátedra a un período académico"""

    catedra = SelectField("Cátedra", choices=[], validators=[DataRequired()])
    grupo = StringField("Grupo", validators=[DataRequired()])
    profesor_id = SelectField("Profesor", coerce=int, validators=[Optional()])
    submit = SubmitField("Asignar")

