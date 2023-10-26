from flask import redirect, url_for, flash, render_template
from flask_login import current_user
from datetime import datetime
from app import model, maps, db
from sqlalchemy import or_
from datetime import datetime, timedelta
import Usuario.forms as formulario


def EsConductor(idUsuario):
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