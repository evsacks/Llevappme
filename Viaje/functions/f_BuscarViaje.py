from flask import redirect, url_for, flash, render_template
from flask_login import current_user
from datetime import datetime
from app import model, maps, db
from sqlalchemy import or_
from datetime import datetime, timedelta
import Viaje.forms as formulario
import random

def comparacion_fecha(fechaInicio,horaInicio):
    if horaInicio:
        fechaInicio0000 = datetime.combine(fechaInicio,horaInicio)
        fechaInicio2359 = datetime.combine(fechaInicio,datetime.strptime('23:59:59', '%H:%M:%S').time())
    else:
        fechaInicio0000 = datetime.combine(fechaInicio,datetime.strptime('00:00:00', '%H:%M:%S').time())
        fechaInicio2359 = datetime.combine(fechaInicio,datetime.strptime('23:59:59', '%H:%M:%S').time())

    return (fechaInicio0000, fechaInicio2359)

def buscar_viaje():
    form = formulario.BuscarViaje()
    resultado = None

    try:
        idUsuario = current_user.get_id()
    
        origen = form.origen.data
        destino = form.destino.data
        fechaInicio = form.fecha_inicio.data
        horaInicio = form.hora_inicio.data

        viajes_query = model.Viaje.query

        if origen:
            # Utiliza una subconsulta para filtrar por ubicaciones que coincidan con el origen.
            ubicaciones_origen = model.Ubicacion.query.filter(model.Ubicacion.direccion_inicial.ilike(f"%{origen}%"))
            viajes_query = viajes_query.filter(model.Viaje.id_ubicacion.in_(u.id for u in ubicaciones_origen))
        
        if destino:
            # Utiliza una subconsulta para filtrar por ubicaciones que coincidan con el destino.
            ubicaciones_destino = model.Ubicacion.query.filter(model.Ubicacion.direccion_final.ilike(f"%{destino}%"))
            viajes_query = viajes_query.filter(model.Viaje.id_ubicacion.in_(u.id for u in ubicaciones_destino))

        if fechaInicio:
            comparacionFecha = comparacion_fecha(fechaInicio, horaInicio)
            fechaInicio0000 = comparacionFecha[0]
            fechaInicio2359 = comparacionFecha[1]
            viajes_query = viajes_query.filter(model.Viaje.fecha_inicio.between(fechaInicio0000, fechaInicio2359))

        viajes = viajes_query.all()

        if not viajes:
            resultado = "No se encontraron resultados"
        else:
            return resultados_busqueda(viajes)
    
    except Exception as e:
        flash(f"Se produjo un error: {str(e)}", 'error')

    return render_template('buscar_viaje.html', resultado=resultado)

def resultados_busqueda(viajes):
    return render_template('resultado_busqueda.html', viajes = viajes)

def obtener_dos_ultimos_viajes():
    # Realiza una consulta para obtener los dos últimos viajes por fecha de creación
    ultimos_viajes = model.Viaje.query.order_by(model.Viaje.id.desc()).limit(2).all()
    
    return ultimos_viajes