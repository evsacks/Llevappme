from app import model, db
from flask_login import login_user,logout_user,login_required,current_user

def esConductor():
    idUsuario = current_user.get_id()
    usuario = model.Usuario.query.get(idUsuario)
    if usuario.id_tipo_usuario == 2:
        return True
    else:
        return False
    
def ConvertirEnPasajero(idUsuario):
    usuario = model.Usuario.query.get(idUsuario)
    # Verificar si el usuario es un conductor
    if usuario.id_tipo_usuario == 2:
        vehiculos_conductor = model.Conductor.query.filter_by(id_usuario=idUsuario).all()
        # Verificar si todos los vehículos están inactivos
        if all(vehiculo.vehiculo.estado_vehiculo.descripcion == 'Inactivo' for vehiculo in vehiculos_conductor):
            # Cambiar el tipo de usuario a pasajero
            usuario.id_tipo_usuario = 1
            db.session.commit()

            # Devolver True para indicar que la conversión fue exitosa
            return True
        else:
            # Devolver False si al menos un vehículo está activo
            return False
    else:
        # Devolver False si el usuario no es un conductor
        return False
    
def ConvertirEnConductor(idUsuario):
    usuario = model.Usuario.query.get(idUsuario)
    if usuario.id_tipo_usuario == 1:
        vehiculo_conductor = model.Conductor.query.filter_by(id_usuario=idUsuario).first()
        if vehiculo_conductor:
            usuario.id_tipo_usuario = 2
            db.session.commit()
            return usuario
    else:
        return False