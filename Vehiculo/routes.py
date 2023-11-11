from flask import Blueprint, render_template, redirect,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime, timedelta
import models as model
import Vehiculo.forms as formulario

import Vehiculo.functions.f_EliminarVehiculo as felv
import Vehiculo.functions.f_NuevoVehiculo as fnuv
import Usuario.functions.f_AccionesUsuario as faccu

vehiculo_bp = Blueprint('vehiculo_bp', __name__, url_prefix='/vehiculo', template_folder='templates', static_folder='static')


#VIAJE SEGUN ESTADO
@vehiculo_bp.route('/', methods=['GET', 'POST'])
@login_required
def Vehiculo():
    form = formulario.CrearVehiculo()
    if form.validate_on_submit():

        patente = form.patente.data.upper()
        cantidad_asientos = form.cantidad_asientos.data
        descripcion = form.descripcion.data

        vehiculo = fnuv.CrearVehiculo(patente,cantidad_asientos,descripcion)
        
        if vehiculo:
            idUsuario = current_user.get_id()
            fnuv.AltaConductor(idUsuario, vehiculo.id)
            flash('Vehiculo creado con éxito.')    
            return redirect(url_for('viaje_bp.BuscarViaje'))
        
        flash('No se ha podido crear el vehiculo.')
        return redirect(url_for('viaje_bp.BuscarViaje'))
    
    return render_template('vehiculo.html', form = form)

@vehiculo_bp.route('/listado', methods=['GET', 'POST'])
@login_required
def ListadoVehiculos():
    idUsuario = current_user.get_id()
    vehiculos = model.Conductor.query.filter_by(id_usuario=idUsuario).all()
    return render_template('listado_vehiculos.html', vehiculos = vehiculos)
    
@vehiculo_bp.route('/eliminar/<idVehiculo>', methods=['GET', 'POST'])
@login_required
def EliminarVehiculo(idVehiculo):

    felv.eliminarVehiculo(idVehiculo)
    convertir = faccu.ConvertirEnPasajero(current_user.id)
    if not convertir:
        flash('Se eliminó el vehiculo del listado de vehiculos.')
        return redirect(url_for('vehiculo_bp.ListadoVehiculos'))
    else:
        flash('Se eliminó el vehiculo del listado de vehiculos. Ahora estás en modo pasajero, para volver a ser un conductor, crea un nuevo vehículo')
        return redirect(url_for('viaje_bp.BuscarViaje'))
