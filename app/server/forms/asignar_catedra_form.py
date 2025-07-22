from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

from app.database.enums import Catedra

class AsignarCatedraForm(FlaskForm):
    catedra = SelectField(
        'Cátedra a asignar',
        choices=Catedra.choices(),
        validators=[DataRequired()],
        render_kw={"class": "form-select"}
    )
    submit = SubmitField('Asignar')
