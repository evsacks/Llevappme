from flask import redirect, url_for, flash
from flask_login import current_user
from datetime import datetime
from app import model

from datetime import datetime
import Usuario.forms as formulario

######################
#### EDITAR usuario ####
######################

def redireccionar_y_mostrar_error(mensaje, tipo, ruta):
    flash(mensaje, tipo)
    return redirect(url_for(ruta))

def actualizar_usuario_con_formulario(usuario, form):
    usuario.nombre = form.nombre.data
    usuario.apellido = form.apellido.data
    usuario.telefono = form.telefono.data
    usuario.fecha_nacimiento = form.fecha_nacimiento.data
    usuario.fecha_actualizacion = datetime.now()

def cargar_datos_del_usuario_en_formulario(form, usuario):
    form.nombre.data = usuario.nombre
    form.apellido.data = usuario.apellido
    form.email.data = usuario.email
    form.telefono.data = usuario.telefono
    form.fecha_nacimiento.data = usuario.fecha_nacimiento
