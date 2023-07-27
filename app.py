from datetime import datetime, timedelta
import os

from flask import Response,Flask, request, jsonify, send_file, render_template, redirect, url_for, flash, send_from_directory, session, send_from_directory
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy, Pagination

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)


@app.route('/', methods=['GET'])
def Login():
    hola = 'Hola Mundo'
    return hola


if __name__ == '__main__':
    app.run(debug=True)
