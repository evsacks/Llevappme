from flask import redirect, url_for, flash
from flask_login import current_user
from datetime import datetime
from app import model

from datetime import datetime
import Viaje.forms as formulario

######################
#### EDITAR VIAJE ####
######################

def tiene_permiso_para_editar(viaje):
    idUsuario = current_user.get_id()
    return int(viaje.conductor.id_usuario) == int(idUsuario)

def redireccionar_y_mostrar_error(mensaje, tipo, ruta):
    flash(mensaje, tipo)
    return redirect(url_for(ruta))

def inicializar_formulario(viaje):
    form = formulario.EditarViaje()
    idUsuario = current_user.get_id()
    conductor = model.Conductor.query.filter_by(id_usuario=idUsuario).all()
    form.vehiculo.choices = [(0, "Vehiculo")] + [(c.id, c.vehiculo.patente) for c in conductor]
    return form

def actualizar_viaje_con_formulario(viaje, form):
    viaje.asientos_disponibles = form.cantidad_asientos.data
    viaje.fecha_inicio = datetime.combine(form.fecha_inicio.data, form.hora_inicio.data)
    viaje.adicional.equipaje = form.equipaje.data
    viaje.adicional.mascota = form.mascota.data
    viaje.adicional.alimentos = form.alimentos.data

def cargar_datos_del_viaje_en_formulario(form, viaje):
    form.origen.data = viaje.ubicacion.direccion_inicial
    form.destino.data = viaje.ubicacion.direccion_final
    form.vehiculo.data = viaje.id_conductor
    form.cantidad_asientos.data = viaje.asientos_disponibles
    form.fecha_inicio.data = viaje.fecha_inicio.date()
    form.hora_inicio.data = viaje.fecha_inicio.time()
    form.equipaje.data = viaje.adicional.equipaje
    form.mascota.data = viaje.adicional.mascota
    form.alimentos.data = viaje.adicional.alimentos
