from flask import redirect, url_for, flash
from flask_login import current_user
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app import model, maps, db

from datetime import datetime, timedelta
import Viaje.forms as formulario

######################
### ELIMINAR VIAJE ###
######################

def eliminar_viaje(viaje):
    idViaje = viaje.id
    viaje.id_estado_viaje = 4
    db.session.commit() 
    
    pasajeros = model.Pasajero.query.filter_by(id_viaje=idViaje).all()
    if pasajeros:
        for pasajero in pasajeros:
            pasajero.id_estado_pasajero = 4
            pasajero.fecha_actualizacion = datetime.now()
            db.session.commit() 
    
    flash('Viaje cancelado con éxito.')

def tiene_permiso_para_eliminar(viaje):
    idUsuario = current_user.get_id()
    return int(viaje.conductor.id_usuario) == int(idUsuario)