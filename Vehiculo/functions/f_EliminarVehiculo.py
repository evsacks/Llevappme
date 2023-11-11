from flask import Blueprint, render_template, url_for, redirect, flash, request, session
import models as model
from flask_login import login_required,current_user
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
import routes as r
import Vehiculo.forms as formulario
from app import maps, db


def eliminarVehiculo(idVehiculo):
    conductor = model.Conductor.query.filter_by(id_vehiculo=idVehiculo).first()
    viajes_conductor = model.Viaje.query.filter_by(id_conductor = conductor.id).all()
    if any(viaje.estado.descripcion == 'Pendiente' for viaje in viajes_conductor):
        flash('No es posible eliminar el vehiculo seleccionado, usted posee viajes pendientes con dicho vehiculo.')
        return False
    if conductor:
        vehiculo = model.Vehiculo.query.get(idVehiculo)

        if vehiculo and vehiculo.id_estado_vehiculo != 'Inactivo':
            desactivado = model.EstadoVehiculo.query.filter_by(descripcion='Inactivo').first().id
            vehiculo.id_estado_vehiculo = desactivado
            db.session.commit()
            return True



