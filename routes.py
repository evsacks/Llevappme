from app import app
from Usuario.routes import usuario_bp
from Viaje.routes import viaje_bp
from Vehiculo.routes import vehiculo_bp

from models import  Usuario, EstadoUsuario, TipoUsuario, LicenciaConducir, Viaje, Tracking, \
                    Pasajero, EstadoPasajero, Vehiculo, Conductor, CedulaConductor, TipoCedula, \
                    SeguroVehiculo, TipoVehiculo, Marca, Modelo, Color

#Blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(vehiculo_bp)
app.register_blueprint(viaje_bp)


#Home
@app.route('/', methods=['GET', 'POST'])
def Home():
    
    return "Hola LLEVAPPME"