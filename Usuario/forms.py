from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField, SubmitField, IntegerField, SelectField, TextAreaField, RadioField
from wtforms.fields.core import BooleanField
from wtforms.fields.html5 import DateField, TimeField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

import models as model

class Login(FlaskForm):
    nombreUsuario = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=2, max=100)])
    contrasenia = PasswordField('Contrasenia',validators=[DataRequired()])
    submit = SubmitField('Ingresar')

class RegistroUsuario(FlaskForm):
    nombreUsuario = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    apellidoUsuario = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefono = IntegerField('Telefono', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired()])
    password = PasswordField('Contraseña', [DataRequired(), EqualTo('confirm', message='Las contraseñas deben coincidir')])
    confirm = PasswordField('Repite la contraseña')
    submit = SubmitField('Registrarse')
