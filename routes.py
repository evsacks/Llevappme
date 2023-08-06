from app import app

from models import  Usuario, EstadoUsuario, TipoUsuario, LicenciaConducir, Viaje, Tracking, \
                    Pasajero, EstadoPasajero, Vehiculo, Conductor, CedulaConductor, TipoCedula, \
                    SeguroVehiculo, TipoVehiculo, Marca, Modelo, Color

@app.route('/', methods=['GET', 'POST'])
def Home():
    
    return "Hola LLEVAPPME"

@app.route('/viajes', methods=['GET', 'POST'])
def Viajes():
    viajes = Viaje.query.all()
    print(viajes)
    return viajes