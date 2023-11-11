from flask import redirect, url_for, flash
from flask_login import current_user
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app import model, maps

from datetime import datetime, timedelta
import Viaje.forms as formulario

######################
### ELIMINAR VIAJE ###
######################

def eliminar_viaje(viaje):
    adicional = viaje.adicional
    ubicacion = viaje.ubicacion
    model.Viaje.delete_from_db(viaje)
    model.Adicional.delete_from_db(adicional)
    model.Ubicacion.delete_from_db(ubicacion)
    flash('Se eliminó el viaje correctamente.')

def tiene_permiso_para_eliminar(viaje):
    idUsuario = current_user.get_id()
    return int(viaje.conductor.id_usuario) == int(idUsuario)