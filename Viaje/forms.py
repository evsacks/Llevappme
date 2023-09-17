from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField, SubmitField, IntegerField, SelectField, TextAreaField, RadioField, BooleanField
from wtforms.fields.html5 import DateField, TimeField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, Optional

import models as model

class NuevoViaje(FlaskForm):
    origen = StringField('Origen', validators=[DataRequired(), Length(min=2, max=100)])
    destino = StringField('Destino', validators=[DataRequired(), Length(min=2, max=100)])
    vehiculo = SelectField('Vehiculo', choices=[], default=0, coerce=int)
    cantidad_asientos = IntegerField('Cantidad de asientos disponibles', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de viaje', validators=[DataRequired()], format='%d/%m/%Y')
    hora_inicio = TimeField('Hora Inicio', validators=[DataRequired()])
    equipaje = BooleanField('Equipaje')
    mascota = BooleanField('Mascota')
    alimentos = BooleanField('Alimentos')
    submit = SubmitField('Finalizar')

class BuscarViaje(FlaskForm):
    origen = StringField('Origen', validators=[Optional(), Length(min=2, max=100)])
    destino = StringField('Destino', validators=[Optional(), Length(min=2, max=100)])
    fecha_inicio = DateField('Fecha de viaje', validators=[Optional()])
    hora_inicio = TimeField('Hora Inicio', validators=[Optional()])
    submit = SubmitField('Buscar')