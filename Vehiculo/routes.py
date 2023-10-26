from flask import Blueprint, render_template, redirect,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime, timedelta
import models as model
import Vehiculo.forms as formulario
vehiculo_bp = Blueprint('vehiculo_bp', __name__, url_prefix='/vehiculo', template_folder='templates', static_folder='static')

def AltaConductor(idUsuario,idVehiculo):
    nuevoConductor = model.Conductor(
        id_usuario=idUsuario,
        id_vehiculo=idVehiculo
    )
    model.Conductor.save_to_db(nuevoConductor)

    usuario = model.Usuario.query.get(idUsuario)
    usuario.id_tipo_usuario = 2
    
    model.Usuario.save_to_db(usuario)

    return nuevoConductor

#VIAJE SEGUN ESTADO
@vehiculo_bp.route('/', methods=['GET', 'POST'])
@login_required
def Vehiculo():
    form = formulario.CrearVehiculo()
    if form.validate_on_submit():

        patente = form.patente.data.upper()
        cantidad_asientos = form.cantidad_asientos.data
        descripcion = form.descripcion.data

        nuevoVehiculo = model.Vehiculo(
            patente=patente,
            cantidad_asientos=cantidad_asientos,
            descripcion = descripcion,
            fecha_actualizacion=datetime.now(),
            fecha_creacion=datetime.now()
        )
        model.Vehiculo.save_to_db(nuevoVehiculo)

        vehiculo = model.Vehiculo.query.get(nuevoVehiculo.id)
        
        if vehiculo:
            idUsuario = current_user.get_id()
            AltaConductor(idUsuario, vehiculo.id)
            
            return redirect(url_for('viaje_bp.BuscarViaje'))
            
        return redirect(url_for('viaje_bp.BuscarViaje'))
    
    return render_template('vehiculo.html', form = form)

@vehiculo_bp.route('/listado', methods=['GET', 'POST'])
@login_required
def ListadoVehiculos():
    idUsuario = current_user.get_id()
    vehiculos = model.Conductor.query.filter_by(id_usuario=idUsuario).all()
    print(vehiculos)
    return render_template('listado_vehiculos.html', vehiculos = vehiculos)
    
@vehiculo_bp.route('/eliminar/<idVehiculo>', methods=['GET', 'POST'])
@login_required
def EliminarVehiculo(idVehiculo):

    conductor = model.Conductor.query.filter_by(id_vehiculo = idVehiculo).first()
    if conductor:
        model.Conductor.delete_from_db(conductor)
        vehiculo = model.Vehiculo.query.get(idVehiculo)
        if vehiculo:
            model.Vehiculo.delete_from_db(vehiculo)

    return redirect(url_for('vehiculo_bp.ListadoVehiculos'))
