from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Optional
from app.database.enums import Calificacion

class CalificacionForm(FlaskForm):
    alumno_id = HiddenField(validators=[InputRequired()])

    nota_final = SelectField(
        "Calificación Final",
        choices=Calificacion.choices(),
        validators=[InputRequired()],
        coerce=str  # Mapeamos el value del enum como string
    )

    observaciones = TextAreaField(
        "Observaciones",
        validators=[Optional()],
        render_kw={"rows": 4, "placeholder": "Comentarios sobre el desempeño, avances, etc."}
    )

    submit = SubmitField("Registrar Calificación")
