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
    
        
