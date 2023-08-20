from flask_wtf import FlaskForm
from wtforms import StringField, DateField ,PasswordField, SubmitField, IntegerField, SelectField, TextAreaField, RadioField
from wtforms.fields.core import BooleanField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

import models as modelo

class NuevoViaje(FlaskForm):
    origen = StringField('Origen', validators=[DataRequired(), Length(min=2, max=100)])
    destino = StringField('Destino', validators=[DataRequired(), Length(min=2, max=100)])
    cantidad_asientos = IntegerField('Cantidad de asientos disponibles', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de viaje', validators=[DataRequired()])
    submit = SubmitField('Finalizar')