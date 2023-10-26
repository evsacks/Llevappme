from flask import Blueprint, render_template, url_for, redirect, flash, request, session
import models as model
from flask_login import login_required,current_user
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
import routes as r
import Vehiculo.forms as formulario
from app import maps, db


def eliminarVehiculo(idVehiculo):
    conductor = model.Conductor.query.filter_by(id_vehiculo = idVehiculo).first()
    if conductor:
        model.Conductor.delete_from_db(conductor)
        vehiculo = model.Vehiculo.query.get(idVehiculo)
        if vehiculo:
            model.Vehiculo.delete_from_db(vehiculo)


