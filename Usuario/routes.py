from flask import Blueprint, render_template, redirect,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime, timedelta

import models as model
import Usuario.forms as formulario

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/usuario', template_folder='templates', static_folder='static')


@usuario_bp.route('/registro', methods=['GET', 'POST'])
def Registro():
    if current_user.is_authenticated:
        return redirect(url_for('viaje_bp.ViajesEstado', estado =3))
    
    form = formulario.RegistroUsuario()
    print("Cargo formulario")
    if form.validate_on_submit():
        print("Validacion ok")
        nombre= form.nombreUsuario.data
        apellido = form.apellidoUsuario.data
        email = form.email.data.strip()
        telefono = form.telefono.data
        fecha_nacimiento = form.fecha_nacimiento.data
        passw = form.password.data

        usuario = model.Usuario.find_by_email(email)

        if usuario:
            return "Ya existe usuario con ese email"
        else:
            nuevoUsuario = model.Usuario(
                nombre=nombre,
                apellido=apellido,
                email=email,
                contrasenia=passw,
                telefono=telefono,
                fecha_nacimiento=fecha_nacimiento,
                fecha_actualizacion=datetime.now(),
                fecha_creacion= datetime.now(),
                id_tipo_usuario=1,
                id_estado_usuario=1
            )
            print(model.Usuario.serialize(nuevoUsuario))
            model.Usuario.save_to_db(nuevoUsuario)

            return redirect(url_for('viaje_bp.ViajesEstado', estado =3))
        
    return render_template('registro.html', form=form)

@usuario_bp.route('/login', methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('viaje_bp.ViajesEstado', estado =3))

    form = formulario.Login()

    if form.validate_on_submit():

        passw = form.contrasenia.data
        email = form.nombreUsuario.data.strip()
        
        usuario = model.Usuario.find_by_email(email)

        if usuario:
            contrasenia = usuario.validar_contrasenia(passw)
            if contrasenia:
                login_user(usuario)
                return redirect(url_for('viaje_bp.ViajesEstado', estado=3))
            else: 
                return "Usuario {}: contraseña incorrecta".format(email)
        else: 
            return "Usuario {} inexistente".format(email)
    return render_template('login.html', form=form)

@usuario_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def Logout():
    logout_user()
    return redirect(url_for('usuario_bp.Login'))


    
