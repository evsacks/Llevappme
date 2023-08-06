import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)

import models
import routes

if __name__ == '__main__':
    app.run(debug=True)
