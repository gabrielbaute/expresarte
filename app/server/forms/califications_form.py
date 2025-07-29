from flask_wtf import FlaskForm
from wtforms import FloatField, HiddenField
from wtforms.validators import InputRequired, NumberRange

class CalificacionForm(FlaskForm):
    alumno_id = HiddenField(validators=[InputRequired()])
    nota_final = FloatField("Nota Final", validators=[
        InputRequired(),
        NumberRange(min=0, max=20, message="La nota debe estar entre 0 y 20")
    ])
