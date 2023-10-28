from flask import redirect, url_for, flash, render_template
from flask_login import current_user
from datetime import datetime
from app import model, maps, db
from sqlalchemy import or_
from datetime import datetime, timedelta
import Viaje.forms as formulario


def modificar_estado_pasajero(idPasajero, nuevo_estado):
    pasajero = model.Pasajero.query.get(idPasajero)

    if pasajero.estado.descripcion in ['Pendiente']:
        estado = model.EstadoPasajero.query.filter_by(descripcion=nuevo_estado).first()
        pasajero.id_estado_pasajero = estado.id
        pasajero.fecha_actualizacion = datetime.now()
        db.session.commit()
        return True
    else:
        mensaje = "No puede modificar el estado del pasajero. Ya fue {}".format(pasajero.estado.descripcion)
        return render_template('grupo_de_viaje.html', viaje=pasajero.viaje, pasajeros = pasajero.viaje.pasajeros, mensaje=mensaje)
           
def viaje_en_curso_como_conductor(idUsuario):
    # Obtén todos los conductores correspondientes al usuario
    conductores = model.Conductor.query.filter_by(id_usuario=idUsuario).all()

    ultimo_viaje_en_curso = None

    for conductor in conductores:
        # Consulta todos los viajes en los que es conductor y que estén en curso
        viaje = model.Viaje.query.filter_by(id_conductor=conductor.id, id_estado_viaje=1).order_by(model.Viaje.id.desc()).first()
        if viaje:
            ultimo_viaje_en_curso = viaje
            return ultimo_viaje_en_curso.id
    return None

def viajes_finalizados_como_conductor(idUsuario):
    # Obtén todos los conductores correspondientes al usuario
    conductores = model.Conductor.query.filter_by(id_usuario=idUsuario).all()

    viajes_finalizados = []

    for conductor in conductores:
        # Consulta todos los viajes en los que es conductor y que estén en curso
        viajes = model.Viaje.query.filter_by(id_conductor=conductor.id, id_estado_viaje=2).all()
        
        # Agrega los viajes a la lista de viajes finalizados
        viajes_finalizados.extend(viajes)

    return viajes_finalizados

def viaje_en_curso_como_pasajero(idUsuario):
    viaje = model.Pasajero.query.filter_by(id_usuario=idUsuario, id_estado_pasajero=5).order_by(model.Pasajero.id.desc()).first()
    if viaje:
        return viaje.id
    else:
        return None
