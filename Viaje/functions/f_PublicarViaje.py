from flask import redirect, url_for, flash
from flask_login import current_user
from datetime import datetime
from app import model, maps
import requests

from datetime import datetime, timedelta
import Viaje.forms as formulario

######################
### PUBLICAR VIAJE ###
######################

def mayorOigualEdad(fecha_objetivo):
    # Obtén la fecha y hora actuales
    fecha_actual = datetime.now()
    # Calcula la diferencia entre la fecha objetivo y la fecha actual
    diferencia = fecha_objetivo - fecha_actual
    
    # Verifica si la fecha objetivo es mayor o igual a la fecha actual
    return diferencia.total_seconds() >= 0

def obtener_datos_del_formulario(form):
    vehiculo = form.vehiculo.data
    origen = form.origen.data
    destino = form.destino.data
    cantidad_asientos = form.cantidad_asientos.data
    fecha_inicio = form.fecha_inicio.data
    hora_inicio = form.hora_inicio.data
    equipaje = form.equipaje.data
    mascota = form.mascota.data
    alimentos = form.alimentos.data

    return vehiculo, origen, destino, cantidad_asientos, fecha_inicio, hora_inicio, equipaje, mascota, alimentos

def obtener_coordenadas_y_distancia(origen, destino):
    coordenadas_origen = maps.geocode(origen)
    coordenadas_destino = maps.geocode(destino)
    matrix_distance = maps.distance_matrix(origen, destino)

    if all('error' not in data for data in [coordenadas_origen, coordenadas_destino, matrix_distance]):
        latitud_origen = coordenadas_origen[0]['geometry']['location']['lat']
        longitud_origen = coordenadas_origen[0]['geometry']['location']['lng']
        latitud_destino = coordenadas_destino[0]['geometry']['location']['lat']
        longitud_destino = coordenadas_destino[0]['geometry']['location']['lng']
        distancia = matrix_distance['rows'][0]['elements'][0]['distance']['text']
        duracion = matrix_distance['rows'][0]['elements'][0]['duration']['value']

        return latitud_origen, longitud_origen, latitud_destino, longitud_destino, distancia, duracion

    return None

def obtener_direccion_desde_coordenadas(latitud, longitud):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitud},{longitud}&key=AIzaSyBPrNn6olS4yqaOK9v7ppvXnu4kXQ_x_98'

    response = requests.get(url)
    data = response.json()

    if 'results' in data and data['results']:
        direccion = data['results'][0]['formatted_address']
        return direccion
    else:
        return None


def guardar_datos_en_la_base_de_datos(vehiculo, origen, destino, cantidad_asientos, fecha_inicio, hora_inicio, latitud_origen, longitud_origen, latitud_destino, longitud_destino, distancia, duracion, equipaje, mascota, alimentos):
    fecha_inicial = datetime.combine(fecha_inicio, hora_inicio)
    fecha_final = fecha_inicial + timedelta(seconds=duracion)

    ubicacion_viaje = model.Ubicacion(
        direccion_inicial=origen,
        direccion_final=destino,
        latitud_inicial=latitud_origen,
        longitud_inicial=longitud_origen,
        latitud_final=latitud_destino,
        longitud_final=longitud_destino
    )

    model.Ubicacion.save_to_db(ubicacion_viaje)

    adicional = model.Adicional(
        equipaje=bool(equipaje),
        mascota=bool(mascota),
        alimentos=bool(alimentos)
    )

    model.Adicional.save_to_db(adicional)

    conductorVehiculo = model.Conductor.query.get(vehiculo)

    nuevo_viaje = model.Viaje(
        asientos_disponibles=cantidad_asientos,
        fecha_inicio=fecha_inicial,
        fecha_final=fecha_final,
        id_conductor=conductorVehiculo.id,
        id_estado_viaje=3,
        fecha_inicio_real=None,
        fecha_final_real=None,
        id_ubicacion=ubicacion_viaje.id,
        id_adicional=adicional.id
    )

    model.Viaje.save_to_db(nuevo_viaje)