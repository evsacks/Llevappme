from flask import Blueprint, render_template, url_for, redirect, flash
import models as model
from flask_login import login_required,current_user
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
import routes as r
import Viaje.forms as formulario
from app import maps, db

import Viaje.functions.f_EditarViaje as fedv
import Viaje.functions.f_EliminarViaje as felv
import Viaje.functions.f_PublicarViaje as fpuv
import Viaje.functions.f_SolicitarViaje as fsov


viaje_bp = Blueprint('viaje_bp', __name__, url_prefix='/viaje', template_folder='templates', static_folder='static')


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

######################    
##### CONDUCTOR ######
######################

@viaje_bp.route('/publicar', methods=['GET', 'POST'])
@login_required
def PublicarViaje():
    try:
        idUsuario = current_user.get_id()
        conductor = model.Conductor.query.filter_by(id_usuario=idUsuario).all()
        form = formulario.NuevoViaje()
        form.vehiculo.choices = [(0, "Vehiculo")] + [(c.id, c.vehiculo.patente) for c in conductor]

        if form.validate_on_submit():
            vehiculo, origen, destino, cantidad_asientos, fecha_inicio, hora_inicio, equipaje, mascota, alimentos = fpuv.obtener_datos_del_formulario(form)
            coordenadas_y_distancia = fpuv.obtener_coordenadas_y_distancia(origen, destino)

            if coordenadas_y_distancia:
                latitud_origen, longitud_origen, latitud_destino, longitud_destino, distancia, duracion = coordenadas_y_distancia

                fpuv.guardar_datos_en_la_base_de_datos(
                    vehiculo, origen, destino, cantidad_asientos, fecha_inicio, hora_inicio,
                    latitud_origen, longitud_origen, latitud_destino, longitud_destino, distancia, duracion,
                    equipaje, mascota, alimentos
                )

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

@viaje_bp.route('/editar/<idViaje>', methods=['GET', 'POST'])
@login_required
def EditarViaje(idViaje):
    viaje = model.Viaje.query.get(idViaje)
    
    if not viaje:
        return fedv.redireccionar_y_mostrar_error('Viaje no encontrado', 'error', 'viaje_bp.ViajesPublicados')
    
    if not fedv.tiene_permiso_para_editar(viaje):
        return fedv.redireccionar_y_mostrar_error('No tienes permiso para editar este viaje', 'error', 'viaje_bp.ViajesPublicados')

    form = fedv.inicializar_formulario(viaje)

    try:
        if form.validate_on_submit():
            fedv.actualizar_viaje_con_formulario(viaje, form)
            db.session.commit()
            flash('Viaje editado con éxito', 'success')
            return redirect(url_for('viaje_bp.VerViaje', idViaje=idViaje))
        else:
            fedv.cargar_datos_del_viaje_en_formulario(form, viaje)
            return render_template('editar_viaje.html', form=form, viaje=viaje)
    except SQLAlchemyError as e:
        flash('Error al editar el viaje', 'error')
        print('Error al editar el viaje:', str(e))
        return redirect(url_for('viaje_bp.ViajesPublicados'))

@viaje_bp.route('/eliminar/<idViaje>', methods=['GET', 'POST'])
@login_required
def EliminarViaje(idViaje):
    viaje = model.Viaje.query.get(idViaje)

    if not viaje:
        return felv.redireccionar_y_mostrar_error('Viaje no encontrado', 'error', 'viaje_bp.BuscarViaje')

    if not felv.tiene_permiso_para_eliminar(viaje):
        return felv.redireccionar_y_mostrar_error('No tienes permiso para eliminar este viaje', 'error', 'viaje_bp.BuscarViaje')

    felv.eliminar_viaje(viaje)

    return redirect(url_for('viaje_bp.BuscarViaje'))

@viaje_bp.route('/publicados', methods=['GET', 'POST'])
@login_required
def ViajesPublicados():
    try:
        idUsuario = current_user.get_id()
        # Busco viajes publicados por ese usuario, es decir siendo conductor.
        conductores = model.Conductor.query.filter_by(id_usuario=idUsuario).all()

        viajes_por_conductor = []

        for conductor in conductores:
            viajes = model.Viaje.query.filter_by(id_conductor=conductor.id).all()
            viajes_por_conductor.extend(viajes)

        if not viajes_por_conductor:
            raise Exception("No se encontraron viajes correspondientes al conductor.")

        return render_template('listado_viajes.html', viajes=viajes_por_conductor)
    except Exception as e:
        # Manejar la excepción si no se encuentran viajes correspondientes.
        print(f"Se produjo una excepción: {e}")
        mensaje = "No hay viajes Publicados."
        return render_template('listado_viajes.html', mensaje=mensaje)

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

######################    
####### AMBOS ########
######################
@viaje_bp.route('/detalle/<idViaje>', methods=['GET', 'POST'])
@login_required
def VerViaje(idViaje):
    try:
        viaje = model.Viaje.query.get(idViaje)
        if not viaje:
            raise Exception("No existe ese viaje")

        idUsuario = current_user.get_id()
        pasajero = fsov.usuario_solicito_viaje(idUsuario,viaje.id)

        if pasajero:
            return render_template('ver_viaje.html', viaje=viaje)
        else:
            return render_template('ver_viaje.html', viaje=viaje, solicitud=True)

    except Exception as e:
        mensaje = str(e)  # Utiliza el mensaje de la excepción para proporcionar información sobre el error
        return render_template('ver_viaje.html', mensaje=mensaje)

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
            resultado = "No se encontraron coincidencias"
        else:
            return resultados_busqueda(viajes)
    
    except Exception as e:
        flash(f"Se produjo un error: {str(e)}", 'error')

    return render_template('buscar_viaje.html', resultado=resultado)

def resultados_busqueda(viajes):
    return render_template('resultado_busqueda.html', viajes = viajes)

######################    
##### PASAJERO #######
######################

@viaje_bp.route('/solicitar/<idViaje>', methods=['GET', 'POST'])
@login_required
def SolicitarViaje(idViaje):
    viaje = model.Viaje.query.get(idViaje)
    idUsuario = current_user.get_id()
    mensaje = None

    if not viaje:
        mensaje = "No existe ese viaje"
    else:
        pasajero = fsov.usuario_solicito_viaje(idUsuario, idViaje)
        conductor = viaje.conductor.id_usuario == idUsuario

        if pasajero:
            mensaje = "Ya solicitaste ese viaje, por favor busca uno nuevo"
        elif conductor:
            mensaje = "Eres el conductor de este viaje"
        else:
            soy_conductor_en = fsov.viajes_pendientes_como_conductor(idUsuario)
            soy_pasajero_en = fsov.viajes_pendientes_como_pasajero(idUsuario)
            mis_viajes = soy_conductor_en + soy_pasajero_en

            if viaje.asientos_disponibles == 0:
                mensaje = 'No hay asientos disponibles'
            elif fsov.hay_conflictos_de_horario(mis_viajes, viaje):
                mensaje = "Ya existe viaje pendiente / confirmado en esa fecha."
            else:
                pasajero = fsov.solicitar_viaje(idUsuario, idViaje)
                if pasajero:
                    mensaje = "Solicitaste el viaje"

    return render_template('ver_viaje.html', viaje=viaje, mensaje=mensaje)


@viaje_bp.route('/ver/solicitudes', methods=['GET', 'POST'])
@login_required
def MisSolicitudes():
    idUsuario = current_user.get_id()
    solicitudesPasajero = model.Pasajero.query.filter_by(id_usuario=idUsuario)
    return render_template('listado_solicitudes.html', solicitudesPasajero=solicitudesPasajero)

@viaje_bp.route('/<idViaje>/pasajeros', methods=['GET', 'POST'])
@login_required
def VerPasajeros(idViaje):
    viaje = model.Viaje.query.get(idViaje)
    return render_template('listado_pasajero_viaje.html', viaje = viaje)
