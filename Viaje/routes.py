from flask import Blueprint, render_template, url_for, redirect
import models as model
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime, timedelta
from sqlalchemy import cast

import Viaje.forms as formulario
from app import maps
from pprint import pprint
viaje_bp = Blueprint('viaje_bp', __name__, url_prefix='/viaje', template_folder='templates', static_folder='static')

def solicitar_viaje(idUsuario,idViaje):
    
    nuevoPasajero = model.Pasajero(
        fecha_actualizacion = datetime.now(),
        fecha_solicitud = datetime.now(),
        id_usuario = idUsuario,
        id_viaje = idViaje,
        id_estado_pasajero = 2
    )

    #viaje = model.Viaje.query.get(idViaje)
    #asientosDisponibles = viaje.asientos_disponibles
    #viaje.asientos_disponibles = asientosDisponibles - 1

    model.Pasajero.save_to_db(nuevoPasajero)
    #model.Viaje.save_to_db(viaje)

    return nuevoPasajero

def comparacion_fecha(fechaInicio,horaInicio):
    print(fechaInicio, horaInicio)
    if horaInicio:
        fechaInicio0000 = datetime.combine(fechaInicio,horaInicio)
        fechaInicio2359 = datetime.combine(fechaInicio,datetime.strptime('23:59:59', '%H:%M:%S').time())
    else:
        fechaInicio0000 = datetime.combine(fechaInicio,datetime.strptime('00:00:00', '%H:%M:%S').time())
        fechaInicio2359 = datetime.combine(fechaInicio,datetime.strptime('23:59:59', '%H:%M:%S').time())
    print(fechaInicio0000)
    print(fechaInicio2359)
    return (fechaInicio0000, fechaInicio2359)

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
    
#PUBLICAR VIAJE - CONDUCTOR
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
                asientos_disponibles= cantidadAsientos,
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
        return render_template('listado_viajes.html', viajes=viajes)
    else: 
        mensaje = "No hay viajes disponibles."
        return render_template('listado_viajes.html', mensaje = mensaje)

@viaje_bp.route('/detalle/<idViaje>', methods=['GET', 'POST'])
@login_required
def VerViaje(idViaje):

    #Busco viajes que estan pendientes 
    viaje = model.Viaje.query.get(idViaje)
    idUsuario = current_user.get_id()
    
    pasajero = model.Pasajero.solicitud_activa(idUsuario,idViaje)

    if viaje:
        if pasajero:
            return render_template('ver_viaje.html', viaje=viaje)
        else:
            return render_template('ver_viaje.html', viaje=viaje, activarSolicitud=True)
    else: 
        mensaje = "No existe ese viaje"
        return render_template('ver_viaje.html', mensaje = mensaje)
    

@viaje_bp.route('/solicitar/<idViaje>', methods=['GET', 'POST'])
@login_required
def SolicitarViaje(idViaje):

    #Busco viajes que estan pendientes 
    viaje = model.Viaje.query.get(idViaje)
    idUsuario = current_user.get_id()
    
    pasajero = model.Pasajero.solicitud_activa(idUsuario,idViaje)
    if pasajero:
        mensaje = "Ya solicitaste ese viaje"
        return redirect(url_for('viaje_bp.ViajesDisponibles'))

    if viaje:

        soyConductor = model.Viaje.viajes_pendientes_usuario(idUsuario) 
        soyPasajero = model.Pasajero.viajes_activos_pasajero(idUsuario)
        
        #Viajes como pasajero y conductor que estan activos o pendientes
        misViajes = soyConductor + soyPasajero
        
        if viaje.asientos_disponibles == 0:
            mensaje = 'No hay asientos disponibles'
            return render_template('ver_viaje.html', mensaje = mensaje)

        if misViajes:
            for v in misViajes:
                coincidencia_inicio = v.fecha_inicio <= viaje.fecha_inicio <= v.fecha_final
                coincidencia_final = v.fecha_inicio <= viaje.fecha_final <= v.fecha_final
                if (coincidencia_inicio or coincidencia_final):
                    mensaje = "Ya existe viaje pendiente / confirmado en esa fecha."
                    return render_template('ver_viaje.html', mensaje = mensaje)

        #Si no hay impedimentos para la solicitud:

        pasajero = solicitar_viaje(idUsuario,idViaje)

        if pasajero: 
            mensaje = "Solicitaste el viaje"
            return render_template('ver_viaje.html', viaje=viaje, mensaje = mensaje)

        return render_template('ver_viaje.html', viaje=viaje)
    else: 
        mensaje = "No existe ese viaje"
        return render_template('ver_viaje.html', mensaje = mensaje)


@viaje_bp.route('/ver/solicitudes', methods=['GET', 'POST'])
@login_required
def VerSolicitudesViaje():
    idUsuario = current_user.get_id()

    solicitudesPasajero = model.Pasajero.query.filter_by(id_usuario=idUsuario)

    return render_template('listado_solicitudes.html', solicitudesPasajero=solicitudesPasajero)


@viaje_bp.route('/buscar', methods=['GET', 'POST'])
@login_required
def BuscarViaje():
    form = formulario.BuscarViaje()
    idUsuario = current_user.get_id()
    viajes = model.Viaje.query.all()
    

    if form.validate_on_submit():
        
        origen = form.origen.data
        destino = form.destino.data
        fechaInicio = form.fecha_inicio.data
        horaInicio = form.hora_inicio.data

        if destino:
            if origen:
                if fechaInicio: #DOF
                    comparacionFecha = comparacion_fecha(fechaInicio, horaInicio)
                    fechaInicio0000 = comparacionFecha[0]
                    fechaInicio2359 = comparacionFecha[1]
                    origen = "%{}%".format(form.origen.data)
                    destino = "%{}%".format(form.destino.data)
                    viajes = model.Viaje.query.filter(
                         (model.Viaje.direccion_inicial.ilike(origen)) & \
                         (model.Viaje.direccion_final.ilike(destino)) & \
                         (model.Viaje.fecha_inicio.between(fechaInicio0000,fechaInicio2359))
                     ).all()
                    resultado = [model.Viaje.serialize(viaje) for viaje in viajes]
                    return render_template('buscar_viaje.html', resultado = resultado)
                else: #DO
                    origen = "%{}%".format(form.origen.data)
                    destino = "%{}%".format(form.destino.data)
                    viajes = model.Viaje.query.filter(
                        (model.Viaje.direccion_inicial.ilike(origen)) & \
                        (model.Viaje.direccion_final.ilike(destino))
                    ).all()
                    resultado = [model.Viaje.serialize(viaje) for viaje in viajes]
                    return render_template('buscar_viaje.html', resultado = resultado)
            else: 
                if fechaInicio: #DF
                    destino = "%{}%".format(form.destino.data)
                    comparacionFecha = comparacion_fecha(fechaInicio, horaInicio)
                    fechaInicio0000 = comparacionFecha[0]
                    fechaInicio2359 = comparacionFecha[1]
                    
                    viajes = model.Viaje.query.filter(
                        (model.Viaje.direccion_final.ilike(destino)) & \
                        (model.Viaje.fecha_inicio.between(fechaInicio0000,fechaInicio2359))
                    ).all()
                    resultado = [model.Viaje.serialize(viaje) for viaje in viajes]
                    return render_template('buscar_viaje.html', resultado = resultado)
                else: #D
                    destino = "%{}%".format(form.destino.data)
                    viajes = model.Viaje.query.filter(
                        (model.Viaje.direccion_final.ilike(destino))
                    ).all()
                    resultado = [model.Viaje.serialize(viaje) for viaje in viajes]
                    return render_template('buscar_viaje.html', resultado = resultado)
        else:
            if origen:
                if fechaInicio: #OF
                    origen = "%{}%".format(form.origen.data)
                    comparacionFecha = comparacion_fecha(fechaInicio, horaInicio)
                    fechaInicio0000 = comparacionFecha[0]
                    fechaInicio2359 = comparacionFecha[1]
                    
                    viajes = model.Viaje.query.filter(
                        (model.Viaje.direccion_inicial.ilike(origen)) & \
                        (model.Viaje.fecha_inicio.between(fechaInicio0000,fechaInicio2359))
                    ).all()
                    resultado = [model.Viaje.serialize(viaje) for viaje in viajes]
                    return render_template('buscar_viaje.html', resultado = resultado)
                else: #O
                    origen = "%{}%".format(form.origen.data)
                    viajes = model.Viaje.query.filter(
                        (model.Viaje.direccion_inicial.ilike(origen))
                    ).all()
                    resultado = [model.Viaje.serialize(viaje) for viaje in viajes]
                    return render_template('buscar_viaje.html', resultado = resultado)
            else:
                if fechaInicio: #F
                    comparacionFecha = comparacion_fecha(fechaInicio, horaInicio)
                    fechaInicio0000 = comparacionFecha[0]
                    fechaInicio2359 = comparacionFecha[1]

                    viajes = model.Viaje.query.filter(
                        (model.Viaje.fecha_inicio.between(fechaInicio0000,fechaInicio2359))
                    ).all()
                    resultado = [model.Viaje.serialize(viaje) for viaje in viajes]
                    return render_template('buscar_viaje.html', resultado = resultado)
                else:
                    resultado = "No hay coincidencias"
                    return render_template('buscar_viaje.html', resultado = resultado)

        # if fechaInicio:
            
            
        #     fechaInicio2359 = datetime.combine(fechaInicio,datetime.strptime('23:59:59', '%H:%M:%S').time())

        #     viajes = model.Viaje.query.filter(
        #                 (model.Viaje.direccion_inicial.ilike(origen)) & \
        #                 (model.Viaje.direccion_final.ilike(destino)) & \
        #                 (model.Viaje.fecha_inicio.between(fechaInicio0000,fechaInicio2359))
        #             ).all()
        #     resultado = [model.Viaje.serialize(viaje) for viaje in viajes]
        #     return render_template('buscar_viaje.html', resultado = resultado)
        # else:
        #     viajes = model.Viaje.query.filter(
        #                 (model.Viaje.direccion_inicial.ilike(origen)) | \
        #                 (model.Viaje.direccion_final.ilike(destino))
        #             ).all()
        #     print(viajes)
        #     resultado = [model.Viaje.serialize(viaje) for viaje in viajes]
        #     return render_template('buscar_viaje.html', resultado = resultado)
    return render_template('buscar_viaje.html', form = form)
