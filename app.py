from datetime import datetime, timedelta
import imp
import json
import os
from traceback import print_tb
import numpy

from sqlalchemy import true

basedir = os.path.abspath(os.path.dirname(__file__))
from flask import Response,Flask, request, jsonify, send_file, render_template, redirect, url_for, flash, send_from_directory, session, send_from_directory
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy, Pagination
from werkzeug.security import generate_password_hash


from flask_uploads import UploadSet, IMAGES, configure_uploads

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
ROWS_PER_PAGE = 5
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
db = SQLAlchemy(app)
api = Api(app)

from models import  Usuario, EstadoUsuario, TipoUsuario, LicenciaConducir, Viaje, Tracking, \
                    Pasajero, EstadoPasajero, Vehiculo, Conductor, CedulaConductor, TipoCedula, \
                    SeguroVehiculo, TipoVehiculo, Marca, Modelo, Color

from authentication import auth

# CONFIGURACION IMAGENES DE LA APLICACION
UPLOAD_RECETAS = os.path.join('static', 'recetas')
UPLOAD_INGREDIENTES = os.path.join('static', 'ingredientes')
app.config["UPLOADED_IMGRECETAS_DEST"] = UPLOAD_RECETAS
app.config["UPLOADED_IMGINGREDIENTES_DEST"] = UPLOAD_INGREDIENTES
imgrecetas = UploadSet('imgrecetas', IMAGES,
                       app.config["UPLOADED_IMGRECETAS_DEST"])
imgingredientes = UploadSet(
    'imgingredientes', IMAGES, app.config["UPLOADED_IMGINGREDIENTES_DEST"])
configure_uploads(app, imgrecetas)
configure_uploads(app, imgingredientes)



@app.route('/', methods=['GET', 'POST'])
def Home():
    return "Hola LLEVAPPME"


if __name__ == '__main__':
    app.run(debug=True)
