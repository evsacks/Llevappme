from flask import Blueprint, render_template
import models as model
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime, timedelta
import Viaje.forms as formulario
from app import maps
from pprint import pprint
viaje_bp = Blueprint('viaje_bp', __name__, url_prefix='/viaje', template_folder='templates', static_folder='static')



#VIAJE SEGUN ESTADO
@viaje_bp.route('/estado/<estado>', methods=['GET', 'POST'])
@login_required
def ViajesEstado(estado):
    idUsuario = current_user.get_id()
    viajes_usuario = model.Viaje.query.filter((model.Viaje.id_conductor==idUsuario) & \
                                       (model.Viaje.id_estado_viaje==estado)).all()
    if viajes_usuario:
        return render_template('viajes_usuario.html',
                               viajes=viajes_usuario)
    else: 
        mensaje = "No hay viajes para el usuario {} en estado {}".\
                format(model.Usuario.query.get(idUsuario).nombre,\
                       model.EstadoViaje.query.get(estado).descripcion)
        return render_template('viajes_usuario.html', mensaje = mensaje)
    
#VIAJES USUARIO
@viaje_bp.route('/todos', methods=['GET', 'POST'])
@login_required
def Viajes():

    idUsuario = current_user.get_id()
    viajes_usuario = model.Viaje.query.filter_by(id_conductor=idUsuario)

    if viajes_usuario:
        return render_template('viajes_usuario.html',
                               viajes=viajes_usuario)
    else: 
        mensaje = "No hay viajes para el usuario {}.".\
                format(model.Usuario.query.get(idUsuario).nombre)
        return render_template('viajes_usuario.html', mensaje = mensaje)
    

#VIAJE SEGUN ESTADO
@viaje_bp.route('/publicar', methods=['GET', 'POST'])
@login_required
def PublicarViaje():
    form = formulario.NuevoViaje()
    idUsuario = current_user.get_id()
    
    if form.validate_on_submit():

        conductor = model.Conductor.query.filter_by(id_usuario=idUsuario).first()
        print(model.Conductor.serialize(conductor))
        if conductor:

            origen = form.origen.data
            destino = form.destino.data
            cantidadAsientos = form.cantidad_asientos.data
            fechaInicio = form.fecha_inicio.data
            horaInicio = form.hora_inicio.data

            fechaInicial = datetime.combine(fechaInicio,horaInicio)
            
            coordenadas_origen = maps.geocode(origen)
            latitud_origen = coordenadas_origen[0]['geometry']['location']['lat']
            longitud_origen = coordenadas_origen[0]['geometry']['location']['lng']

            coordenadas_destino = maps.geocode(destino)
            latitud_destino = coordenadas_destino[0]['geometry']['location']['lat']
            longitud_destino = coordenadas_destino[0]['geometry']['location']['lng']
            
            matrix_distance = maps.distance_matrix(origen,destino)
            distancia = matrix_distance['rows'][0]['elements'][0]['distance']['value']
            duracion = matrix_distance['rows'][0]['elements'][0]['duration']['value']

            fechaFinal = fechaInicial + timedelta(seconds=duracion)

            nuevoViaje = model.Viaje(
                cantidad_pasajeros= cantidadAsientos,
                distancia=distancia,
                direccion_inicial=origen,
                direccion_final=destino,
                latitud_inicial=latitud_origen,
                longitud_inicial=longitud_origen,
                latitud_final=latitud_destino,
                longitud_final=longitud_destino,
                fecha_inicio=fechaInicial,
                fecha_final=fechaFinal,
                id_conductor=conductor.id_usuario,
                id_vehiculo=conductor.id_vehiculo,
                id_estado_viaje=3,
                fecha_inicio_real=None,
                fecha_final_real=None
            ) 
            model.Viaje.save_to_db(nuevoViaje)
            return 'OK'
        return 'NO EXISTE CONDUCTOR'

    return render_template('publicar_viaje.html', form = form)

@viaje_bp.route('/disponibles', methods=['GET', 'POST'])
@login_required
def ViajesDisponibles():

    #Busco viajes que estan pendientes 
    viajes = model.Viaje.query.filter_by(id_estado_viaje=3)

    if viajes:
        return render_template('listado_viajes.html',
                               viajes=viajes)
    else: 
        mensaje = "No hay viajes disponibles."
        return render_template('listado_viajes.html', mensaje = mensaje)

@viaje_bp.route('/detalle/<idViaje>', methods=['GET', 'POST'])
@login_required
def VerViaje(idViaje):

    #Busco viajes que estan pendientes 
    viaje = model.Viaje.query.get(idViaje)

    if viaje:
        return render_template('ver_viaje.html',
                               viaje=viaje)
    else: 
        mensaje = "No existe ese viaje"
        return render_template('ver_viaje.html', mensaje = mensaje)
    

@viaje_bp.route('/solicitar/<idViaje>', methods=['GET', 'POST'])
@login_required
def SolicitarViaje(idViaje):

    #Busco viajes que estan pendientes 
    viaje = model.Viaje.query.get(idViaje)
    idUsuario = current_user.get_id()

    if viaje:

        soyConductor = model.Viaje.viajes_pendientes_usuario(idUsuario) 
        soyPasajero = model.Pasajero.viajes_activos_pasajero(idUsuario)
        print(soyConductor)
        print(soyPasajero)
        misViajes = soyConductor + soyPasajero
        print(misViajes)
        #for viaje in misViajes:
            #if viaje.fecha_inicio 

        return render_template('ver_viaje.html',
                               viaje=viaje)
    else: 
        mensaje = "No existe ese viaje"
        return render_template('ver_viaje.html', mensaje = mensaje)
