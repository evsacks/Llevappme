from flask import redirect, url_for, flash, render_template
from flask_login import current_user
from datetime import datetime
from app import model, maps, db
from sqlalchemy import or_
from datetime import datetime, timedelta
import Viaje.forms as formulario

# Función auxiliar para comprobar si un usuario ya ha solicitado un viaje
def usuario_solicito_viaje(idUsuario, idViaje):
    pasajero = model.Pasajero.query.filter_by(id_usuario=idUsuario, id_viaje=idViaje, id_estado_pasajero=3)\
                                    .first()
    return pasajero is not None

# Función auxiliar para verificar si hay conflictos de horario entre viajes
def hay_conflictos_de_horario(mis_viajes, viaje):
    for v in mis_viajes:
        coincidencia_inicio = v.fecha_inicio <= viaje.fecha_inicio <= v.fecha_final
        coincidencia_final = v.fecha_inicio <= viaje.fecha_final <= v.fecha_final
        if coincidencia_inicio or coincidencia_final:
            return True
    return False

def solicitar_viaje(idUsuario,idViaje):
    
    nuevoPasajero = model.Pasajero(
        fecha_actualizacion = datetime.now(),
        fecha_solicitud = datetime.now(),
        id_usuario = idUsuario,
        id_viaje = idViaje,
        id_estado_pasajero = 2
    )

    viaje = model.Viaje.query.get(idViaje)
    asientosDisponibles = viaje.asientos_disponibles
    viaje.asientos_disponibles = asientosDisponibles - 1

    model.Pasajero.save_to_db(nuevoPasajero)
    db.session.commit()

    return nuevoPasajero

def viajes_pendientes_como_conductor(idUsuario):
    # Obtén todos los conductores correspondientes al usuario
    conductores = model.Conductor.query.filter_by(id_usuario=idUsuario).all()

    viajes_pendientes = []

    for conductor in conductores:
        # Consulta todos los viajes en los que es conductor y que estén pendientes
        viajes = model.Viaje.query.filter_by(id_conductor=conductor.id, id_estado_viaje=3).all()
        viajes_pendientes.extend(viajes)

    return viajes_pendientes

def viajes_pendientes_como_pasajero(idUsuario):
    # Consulta todos los viajes en los que eres pasajero y que estén pendientes o confirmados
    pasajeros = model.Pasajero.query.filter_by(id_usuario=idUsuario)\
                                    .filter(or_(model.Pasajero.id_estado_pasajero == 1, \
                                                model.Pasajero.id_estado_pasajero == 2))\
                                    .all()

    # Recopila los VIAJES para retornarlos.
    viajes_pendientes = [pasajero.viaje for pasajero in pasajeros]

    return viajes_pendientes

def pasajeros_pendientes_viaje(idViaje):
    # Consulta todos los pasajeros de un viaje que estén pendientes o confirmados
    pasajeros = model.Pasajero.query.filter_by(id_viaje=idViaje)\
                                    .filter(or_(model.Pasajero.id_estado_pasajero == 1, \
                                                model.Pasajero.id_estado_pasajero == 2))\
                                    .all()
    return pasajeros