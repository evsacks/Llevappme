from flask import Blueprint, render_template, url_for, redirect, flash, request, session
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
import Viaje.functions.f_SolicitudViaje as fsov
import Viaje.functions.f_AccionesConductor as facc
import Viaje.functions.f_BuscarViaje as fbuv
import Viaje.functions.f_IniciarViaje as finv

viaje_bp = Blueprint('viaje_bp', __name__, url_prefix='/viaje', template_folder='templates', static_folder='static')
 


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
            return render_template('publicar_viaje.html', form=form)
    except Exception as e:
        print(f"Se produjo una excepción: {e}")
        flash('No se pudo publicar el viaje. Inténtalo de nuevo más tarde.')
        return render_template('publicar_viaje.html', form=form)

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
        return render_template('listado_viajes.html')

@viaje_bp.route('pasajero/<idPasajero>/confirmar', methods=['GET', 'POST'])
@login_required
def AceptarPasajero(idPasajero):
    if facc.modificar_estado_pasajero(idPasajero, 'Confirmado'):
        pasajero = model.Pasajero.query.get(idPasajero)
        asientosActuales = pasajero.viaje.asientos_disponibles
        pasajero.viaje.asientos_disponibles = asientosActuales - 1
        db.session.commit()
    return redirect(url_for('viaje_bp.GrupoDeViaje', idViaje=pasajero.id_viaje))

@viaje_bp.route('pasajero/<idPasajero>/rechazar', methods=['GET', 'POST'])
@login_required
def RechazarPasajero(idPasajero):
    pasajero = model.Pasajero.query.get(idPasajero)
    if facc.modificar_estado_pasajero(idPasajero, 'Rechazado'):
        return redirect(url_for('viaje_bp.GrupoDeViaje', idViaje=pasajero.id_viaje))

@viaje_bp.route('/<idViaje>/pasajeros/<idEstado>', methods=['GET', 'POST'])
@login_required
def VerPasajeros(idViaje, idEstado):
    viaje = model.Viaje.query.get(idViaje)
    #Estado 2 = Pendiente
    #Estado 3 = Rechazado
    #Estado 4 = Cancelado
    pasajeros = fsov.pasajeros_viaje(idViaje, idEstado)

    return render_template('pasajeros_viaje.html', pasajeros = pasajeros, viaje = viaje)


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
        es_pasajero = fsov.usuario_solicito_viaje(idUsuario,viaje.id)
        coordenadas_y_distancia = fpuv.obtener_coordenadas_y_distancia(viaje.ubicacion.direccion_inicial, viaje.ubicacion.direccion_final)
        _, _, _, _, distancia, duracion = coordenadas_y_distancia

        if es_pasajero: 
            return render_template('ver_viaje.html', viaje=viaje, solicitud="Enviada", fechaInicio = viaje.fecha_inicio, distancia = distancia, duracion = duracion)
        else:
            return render_template('ver_viaje.html', viaje=viaje, solicitud="Libre", fechaInicio = viaje.fecha_inicio, distancia = distancia, duracion = duracion)

    except Exception as e:
        mensaje = str(e) 
        return render_template('ver_viaje.html', fechaInicio = viaje.fecha_inicio)

@viaje_bp.route('/buscar', methods=['GET', 'POST'])
@login_required
def BuscarViaje():
    form = formulario.BuscarViaje()
    if form.validate_on_submit():
        return fbuv.buscar_viaje()
    viajes = fbuv.obtener_dos_ultimos_viajes()
    return render_template('buscar_viaje.html', form=form, viajes = viajes)

@viaje_bp.route('/<idViaje>/grupo', methods=['GET', 'POST'])
@login_required
def GrupoDeViaje(idViaje):
    viaje = model.Viaje.query.get(idViaje)
    pasajerosConfirmados = fsov.pasajeros_viaje(idViaje, 1)
    pasajerosEnViaje = fsov.pasajeros_viaje(idViaje, 5)
    pasajeros = pasajerosConfirmados + pasajerosEnViaje
    return render_template('grupo_de_viaje.html', pasajeros = pasajeros, viaje = viaje)

@viaje_bp.route('/<idViaje>/iniciar', methods=['GET', 'POST'])
@login_required
def IniciarViaje(idViaje):
    viaje = model.Viaje.query.get(idViaje)
    return render_template('iniciar_viaje.html', viaje=viaje)

@viaje_bp.route('/<idViaje>/confirmar', methods=['GET', 'POST'])
@login_required
def ConfirmarInicioViaje(idViaje):
    viaje = model.Viaje.query.get(idViaje)
    pasajerosConfirmados = request.form.getlist("grupo-viaje")

    for p in pasajerosConfirmados:
        pasajero = model.Pasajero.query.get(p)
        finv.confirmarPasajero(pasajero.id)
        finv.iniciarViaje(idViaje)
    
    return redirect(url_for('viaje_bp.VerViaje', idViaje = idViaje))
    
@viaje_bp.route('/<idViaje>/finalizar', methods=['GET', 'POST'])
@login_required
def FinalizarViaje(idViaje):
    viaje = model.Viaje.query.get(idViaje)
    if viaje:

        pasajeros = model.Pasajero.query.filter_by(id_viaje = idViaje, id_estado_pasajero = 5).all()
        for pasajero in pasajeros:
            pasajero.id_estado_pasajero = 6
            pasajero.fecha_actualizacion = datetime.now()
            db.session.commit()

        viaje.fecha_final_real = datetime.now()
        viaje.id_estado_viaje = 2
        db.session.commit()

        return redirect(url_for('viaje_bp.VerViaje', idViaje = idViaje))

@viaje_bp.route('/activar/ubicacion', methods=['GET', 'POST'])
@login_required
def ActivarUbicacion():
    session['ubicacion_activada'] = True
    return redirect(url_for('viaje_bp.BuscarViaje'))

@viaje_bp.route('/desactivar/ubicacion', methods=['GET', 'POST'])
@login_required
def DesactivarUbicacion():
    session['ubicacion_activada'] = False
    return redirect(url_for('viaje_bp.BuscarViaje'))

######################    
##### PASAJERO #######
######################

@viaje_bp.route('/solicitud/<idViaje>', methods=['GET', 'POST'])
@login_required
def SolicitudViaje(idViaje):
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
                    return redirect(url_for("viaje_bp.VerViaje", idViaje = idViaje))

    return render_template('ver_viaje.html', viaje=viaje)

@viaje_bp.route('/cancelar/solicitud/<idViaje>', methods=['GET', 'POST'])
@login_required
def CancelarSolicitudViaje(idViaje):
    viaje = model.Viaje.query.get(idViaje)
    idUsuario = current_user.get_id()
    mensaje = None

    if not viaje:
        mensaje = "No existe ese viaje"
    else:
        pasajero = fsov.usuario_solicito_viaje(idUsuario, idViaje)
        conductor = viaje.conductor.id_usuario == idUsuario
        if conductor:
            mensaje = "Eres el conductor de este viaje"
        elif pasajero:
            pasajero_cancelado = fsov.cancelar_solicitud_viaje(idUsuario, idViaje)
            mensaje = "cancelaste tu solicitud"
            return redirect(url_for("viaje_bp.VerViaje", idViaje = idViaje))
        else:
            return redirect(url_for("viaje_bp.VerViaje", idViaje = idViaje))
    return render_template('ver_viaje.html', viaje=viaje)

@viaje_bp.route('/ver/solicitudes', methods=['GET', 'POST'])
@login_required
def MisSolicitudes():
    idUsuario = current_user.get_id()
    solicitudesPasajero = model.Pasajero.query.filter_by(id_usuario=idUsuario)
    return render_template('listado_solicitudes.html', solicitudesPasajero=solicitudesPasajero)

@viaje_bp.route("/finalizados", methods=["get"])
@login_required
def ViajesFinalizados():
    idUsuario = current_user.get_id()
    viajesPasajero = model.Pasajero.query.filter_by(id_usuario = idUsuario, id_estado_pasajero = 6).all()
    viajesConductor = facc.viajes_finalizados_como_conductor(idUsuario)
    return render_template('viajes_finalizados.html', viajesPasajero = viajesPasajero, viajesConductor = viajesConductor)

@viaje_bp.route("/guardar/ubicacion", methods=["POST"])
@login_required
def GuardarUbicacion():
    
    data = request.get_json()
    latitud = data["latitud"]
    longitud = data["longitud"]
    idViaje = data["idViaje"]
    
    tracking = model.Tracking(latitud= latitud,
                              longitud= longitud,
                              id_viaje= idViaje,
                              fecha= datetime.now())
    model.Tracking.save_to_db(tracking)
    
    return "Ubicación guardada con éxito", 200

