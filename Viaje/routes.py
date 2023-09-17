from flask import Blueprint, render_template, url_for, redirect, flash
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
       
#PUBLICAR VIAJE - CONDUCTOR
@viaje_bp.route('/publicar', methods=['GET', 'POST'])
@login_required
def PublicarViaje():
    try:
        idUsuario = current_user.get_id()
        conductor = model.Conductor.query.filter_by(id_usuario=idUsuario).all()
        form = formulario.NuevoViaje()
        form.vehiculo.choices = [(0, "Vehiculo")] + [(c.id, c.vehiculo.patente) for c in conductor]

        if form.validate_on_submit():
            vehiculo = form.vehiculo.data
            conductorVehiculo = model.Conductor.query.get(vehiculo)

            if conductorVehiculo:
                origen = form.origen.data
                destino = form.destino.data
                cantidad_asientos = form.cantidad_asientos.data
                fecha_inicio = form.fecha_inicio.data
                hora_inicio = form.hora_inicio.data
                fecha_inicial = datetime.combine(fecha_inicio, hora_inicio)

                coordenadas_origen = maps.geocode(origen)
                coordenadas_destino = maps.geocode(destino)
                matrix_distance = maps.distance_matrix(origen, destino)

                if all('error' not in data for data in [coordenadas_origen, coordenadas_destino, matrix_distance]):
                    latitud_origen = coordenadas_origen[0]['geometry']['location']['lat']
                    longitud_origen = coordenadas_origen[0]['geometry']['location']['lng']
                    latitud_destino = coordenadas_destino[0]['geometry']['location']['lat']
                    longitud_destino = coordenadas_destino[0]['geometry']['location']['lng']
                    distancia = matrix_distance['rows'][0]['elements'][0]['distance']['value']
                    duracion = matrix_distance['rows'][0]['elements'][0]['duration']['value']

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
                        equipaje=bool(form.equipaje.data),
                        mascota=bool(form.mascota.data),
                        alimentos=bool(form.alimentos.data)
                    )

                    model.Adicional.save_to_db(adicional)

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

                    flash('Viaje publicado con éxito', 'success')
                    return redirect(url_for('viaje_bp.BuscarViaje'))
                else:
                    flash('Hubo un error al obtener detalles de ubicación o distancia', 'error')
            else:
                flash('No existe conductor asociado', 'error')
        
        return render_template('publicar_viaje.html', form=form)
    except Exception as e:
        print(f"Se produjo una excepción: {e}")
        mensaje = "No se pudo publicar el viaje. Inténtalo de nuevo más tarde."
        return render_template('publicar_viaje.html', mensaje=mensaje)


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

    viaje = model.Viaje.query.get(idViaje)
    idUsuario = current_user.get_id()
    
    pasajero = model.Pasajero.solicitud_activa(idUsuario,idViaje)

    if viaje:
        if pasajero:
            return render_template('ver_viaje.html', viaje=viaje)
        else:
            return render_template('ver_viaje.html', viaje=viaje, solicitud = True)
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
        mensaje = "Ya solicitaste ese viaje, por favor busca uno nuevo"
        return redirect(url_for('viaje_bp.BuscarViaje'))

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
def MisSolicitudes():
    idUsuario = current_user.get_id()
    solicitudesPasajero = model.Pasajero.query.filter_by(id_usuario=idUsuario)
    return render_template('listado_solicitudes.html', solicitudesPasajero=solicitudesPasajero)

@viaje_bp.route('/buscar', methods=['GET', 'POST'])
@login_required
def BuscarViaje():
    form = formulario.BuscarViaje()
    if form.validate_on_submit():
        print("validado, dispara buscar_viaje()")
        return buscar_viaje()
    return render_template('buscar_viaje.html', form=form)

def buscar_viaje():
    form = formulario.BuscarViaje()
    idUsuario = current_user.get_id()
    
    origen = form.origen.data
    destino = form.destino.data
    fechaInicio = form.fecha_inicio.data
    horaInicio = form.hora_inicio.data

    viajes_query = model.Viaje.query

    if origen:
        viajes_query = viajes_query.filter(model.viaje.ubicacion.direccion_inicial.ilike(f"%{origen}%"))
    
    if destino:
        viajes_query = viajes_query.filter(model.viaje.ubicacion.direccion_final.ilike(f"%{destino}%"))

    if fechaInicio:
        comparacionFecha = comparacion_fecha(fechaInicio, horaInicio)
        fechaInicio0000 = comparacionFecha[0]
        fechaInicio2359 = comparacionFecha[1]
        viajes_query = viajes_query.filter(model.Viaje.fecha_inicio.between(fechaInicio0000, fechaInicio2359))

    viajes = viajes_query.all()
    if viajes:
        return resultados_busqueda(viajes)
    else:
        resultado = "No se encontraron coincidencias"
    return render_template('buscar_viaje.html', resultado=resultado)

def resultados_busqueda(viajes):
    return render_template('resultado_busqueda.html', viajes = viajes)

@viaje_bp.route('/publicados', methods=['GET', 'POST'])
@login_required
def ViajesPublicados():
    try:
        idUsuario = current_user.get_id()
        # Busco viajes publicados por ese usuario, es decir siendo conductor.
        conductores = model.Conductor.query.filter_by(id_usuario=idUsuario).all()
        print(conductores)
        viajes_por_conductor = []

        for conductor in conductores:
            viajes = model.Viaje.query.filter_by(id_conductor=conductor.id).all()
            viajes_por_conductor.extend(viajes)
        print(viajes_por_conductor)

        if not viajes_por_conductor:
            raise Exception("No se encontraron viajes correspondientes al conductor.")

        return render_template('listado_viajes.html', viajes=viajes_por_conductor)
    except Exception as e:
        # Manejar la excepción si no se encuentran viajes correspondientes.
        print(f"Se produjo una excepción: {e}")
        mensaje = "No hay viajes Publicados."
        return render_template('listado_viajes.html', mensaje=mensaje)

    
@viaje_bp.route('/<idViaje>/pasajeros', methods=['GET', 'POST'])
@login_required
def VerPasajeros(idViaje):
    viaje = model.Viaje.query.get(idViaje)
    return render_template('listado_pasajero_viaje.html', viaje = viaje)

def modificar_estado_pasajero(idPasajero, idViaje, nuevo_estado):
    pasajero = model.Pasajero.query.get(idPasajero)

    if pasajero.estado.descripcion in ['Rechazado', 'Confirmado']:
        viaje = model.Viaje.query.get(idViaje)
        
        mensaje = "No puede modificar el estado del pasajero. Ya fue {}".format(pasajero.estado.descripcion)
        return render_template('listado_pasajero_viaje.html', viaje=viaje, mensaje=mensaje)
    
    else:
        estado = model.EstadoPasajero.query.filter_by(descripcion=nuevo_estado).first()
        pasajero.id_estado_pasajero = estado.id
        pasajero.fecha_actualizacion = datetime.now()
        model.Pasajero.save_to_db(pasajero)
        return True

@viaje_bp.route('/<idViaje>/pasajero/<idPasajero>/confirmar', methods=['GET', 'POST'])
@login_required
def AceptarPasajero(idPasajero, idViaje):
    if modificar_estado_pasajero(idPasajero, idViaje, 'Confirmado'):
        viaje = model.Viaje.query.get(idViaje)
        asientosActuales = viaje.asientos_disponibles
        viaje.asientos_disponibles = asientosActuales - 1
        model.Viaje.save_to_db(viaje)
    return redirect(url_for('viaje_bp.VerPasajeros', idViaje=viaje.id))

@viaje_bp.route('/<idViaje>/pasajero/<idPasajero>/rechazar', methods=['GET', 'POST'])
@login_required
def RechazarPasajero(idPasajero, idViaje):
    modificar_estado_pasajero(idPasajero, idViaje, 'Rechazado')
    return redirect(url_for('viaje_bp.VerPasajeros', idViaje=idViaje))