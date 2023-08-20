from flask import Blueprint, render_template
import models as model
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime, timedelta
import Viaje.forms as formulario
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
    
#VIAJE SEGUN ESTADO
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
@viaje_bp.route('/todos', methods=['GET', 'POST'])
@login_required
def PublicarViaje():
    form = formulario.NuevoViaje()

    if form.validate_on_submit():
        origen = form.origen.data
        destino = form.destino.data
        asientos = form.cantidad_asientos.data
        fecha_inicio = form.fecha_inicio.data

        validarViajeUsuario = model.Viaje.query.filter((model.Viaje.id_conductor == current_user.get_id()) \
                                                        & (model.Viaje.fecha_inicio == fecha_inicio))
        
        if validarViajeUsuario:
            return "El usuario ya presenta un viaje para esa fecha especificada"
        else:
            crearViaje = model.Viaje(
                cantidad_pasajeros=asientos,
                
            )

        return

    return