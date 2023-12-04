from datetime import datetime
from app import model, db
from datetime import datetime

def confirmarPasajero(idPasajero):
    pasajero = model.Pasajero.query.get(idPasajero)
    pasajero.id_estado_pasajero = 5
    pasajero.fecha_actualizacion = datetime.now()
    db.session.commit()
    return True

def iniciarViaje(idViaje):
    viaje = model.Viaje.query.get(idViaje)
    viaje.fecha_inicio_real = datetime.now()
    viaje.id_estado_viaje = 1
    db.session.commit()
    return cancelarIncumplidos(idViaje)

def cancelarIncumplidos(idViaje):
    pasajerosIncumplidos = model.Pasajero.query.filter_by(id_viaje=idViaje, id_estado_pasajero=1).all()
    if pasajerosIncumplidos:
        for pasajero in pasajerosIncumplidos:
            pasajero.id_estado_pasajero = 4
            pasajero.fecha_actualizacion = datetime.now()
            db.session.commit() 
    return True