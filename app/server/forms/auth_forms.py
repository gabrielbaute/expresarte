from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    """Formulario para inicio de sesión de usuarios"""
    
    email = StringField(
        'Correo electrónico',
        validators=[
            DataRequired(message="Este campo es obligatorio."),
            Email(message="Introduce un correo válido."),
            Length(max=100)
        ]
    )
    
    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message="Este campo es obligatorio."),
            Length(min=6, max=128, message="La contraseña debe tener entre 6 y 128 caracteres.")
        ]
    )

    submit = SubmitField('Iniciar sesión')
