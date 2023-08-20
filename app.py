import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import googlemaps
from pprint import pprint
API_KEY = 'AIzaSyDt5KdV_gWgU2L_W7yNsJucH5XvQ_dcHq0'
#basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)

login_manager = LoginManager(app)
login_manager.login_view = "usuario_bp.Login"

import models as modelo
import routes as rutas

maps = googlemaps.Client(API_KEY)

#direccion = 'Pilar, Buenos Aires'
#response = maps.geocode(direccion)
#pprint(response)

if __name__ == '__main__':
    app.run(debug=True)
