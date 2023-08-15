import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
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

if __name__ == '__main__':
    app.run(debug=True)
