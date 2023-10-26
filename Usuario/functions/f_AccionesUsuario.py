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
    if usuario.id_tipo_usuario == 2:
        vehiculo_conductor = model.Conductor.query.filter_by(id_usuario=idUsuario).first()
        if not vehiculo_conductor:
            usuario.id_tipo_usuario = 1
            db.session.commit()
            return usuario
    else:
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