from flask import Blueprint, render_template, redirect,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime, timedelta
import models as modelo
import Vehiculo.forms as formulario
vehiculo_bp = Blueprint('vehiculo_bp', __name__, url_prefix='/vehiculo', template_folder='templates', static_folder='static')

def AltaConductor(idUsuario,idVehiculo):
    nuevoConductor = modelo.Conductor(
        id_usuario=idUsuario,
        id_vehiculo=idVehiculo
    )
    modelo.Conductor.save_to_db(nuevoConductor)
    return nuevoConductor

#VIAJE SEGUN ESTADO
@vehiculo_bp.route('/', methods=['GET', 'POST'])
@login_required
def Vehiculo():
    form = formulario.CrearVehiculo()
    if form.validate_on_submit():

        patente = form.patente.data
        cantidad_asientos = form.cantidad_asientos.data
        descripcion = form.descripcion.data

        nuevoVehiculo = modelo.Vehiculo(
            patente=patente,
            cantidad_asientos=cantidad_asientos,
            descripcion = descripcion,
            fecha_actualizacion=datetime.now(),
            fecha_creacion=datetime.now()
        )
        modelo.Vehiculo.save_to_db(nuevoVehiculo)

        vehiculo = modelo.Vehiculo.get(nuevoVehiculo.id)
        
        if vehiculo:
            idUsuario = current_user.get_id()
            AltaConductor(idUsuario, vehiculo.id)
            
            return redirect(url_for('viaje_bp.ViajesEstado', estado =3))
            
        return redirect(url_for('viaje_bp.ViajesEstado', estado =3))
    
    return render_template('vehiculo.html', form = form)

@vehiculo_bp.route('/listado', methods=['GET', 'POST'])
@login_required
def ListadoVehiculos():
    vehiculos = modelo.Conductor.query.filter_by(id_usuario=current_user.get_id())
    return render_template('listado_vehiculos.html', vehiculos = vehiculos)
    
