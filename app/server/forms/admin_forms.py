from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length

from app.database.enums import Sexo, Role, Estatus

class CreateUserForm(FlaskForm):
    """Formulario para crear usuarios"""

    primer_nombre = StringField('Primer Nombre', validators=[DataRequired(), Length(max=50)])
    segundo_nombre = StringField('Segundo Nombre', validators=[DataRequired(), Length(max=50)])
    primer_apellido = StringField('Primer Apellido', validators=[DataRequired(), Length(max=50)])
    segundo_apellido = StringField('Segundo Apellido', validators=[DataRequired(), Length(max=50)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6, max=128)])
    sexo = SelectField('Sexo', choices=Sexo.choices(), validators=[DataRequired()])
    role = SelectField('Rol', choices=Role.choices(), validators=[DataRequired()])
    cedula = StringField('Cédula', validators=[Length(max=20)])  # Si decides hacerlo obligatorio, se le añade DataRequired
    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d', validators=[DataRequired()])
    # activo = BooleanField('Activo', choices=Estatus.choices(), default=True)
    submit = SubmitField('Crear Usuario')
