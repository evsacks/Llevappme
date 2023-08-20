from flask_wtf import FlaskForm
from wtforms import StringField, DateField ,PasswordField, SubmitField, IntegerField, SelectField, TextAreaField, RadioField
from wtforms.fields.core import BooleanField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField

import models as model

class CrearVehiculo(FlaskForm):
    patente = StringField('Patente', validators=[DataRequired(), Length(min=6, max=7)])
    cantidad_asientos = IntegerField('Cantidad de asientos', validators=[DataRequired()])
    descripcion = StringField('Descripcion', validators=[DataRequired(), Length(min=10, max=100)])
    submit = SubmitField('Agregar Vehiculo')
