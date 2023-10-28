from flask import Blueprint, render_template, redirect,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime, timedelta

import models as model
import Usuario.forms as formulario
import Usuario.functions.f_perfil as fper

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/usuario', template_folder='templates', static_folder='static')


@usuario_bp.route('/registro', methods=['GET', 'POST'])
def Registro():
    if current_user.is_authenticated:
        return redirect(url_for('viaje_bp.BuscarViaje'))
    
    form = formulario.RegistroUsuario()
    print("Cargo formulario")
    if form.validate_on_submit():

        nombre= form.nombreUsuario.data
        apellido = form.apellidoUsuario.data
        email = form.email.data.strip()
        telefono = form.telefono.data
        fecha_nacimiento = form.fecha_nacimiento.data
        passw = form.password.data

        usuario_email = model.Usuario.find_by_email(email)
        usuario_telefono = model.Usuario.find_by_telefono(telefono)


        if usuario_email or usuario_telefono:
            flash("El email o teléfono especificado ya esta en uso")
            return render_template('registro.html', form=form)
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
            flash("Usuario creado exitosamente, ingrese sus credenciales para iniciar.")
            return redirect(url_for('viaje_bp.Login'))
        
    return render_template('registro.html', form=form)

@usuario_bp.route('/login', methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('viaje_bp.BuscarViaje'))

    form = formulario.Login()

    if form.validate_on_submit():

        passw = form.contrasenia.data
        email = form.nombreUsuario.data.strip()
        
        usuario = model.Usuario.find_by_email(email)

        if usuario:
            contrasenia = usuario.validar_contrasenia(passw)
            if contrasenia:
                login_user(usuario)
                return redirect(url_for('viaje_bp.BuscarViaje'))
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


@usuario_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
def Perfil():
    idUsuario = current_user.get_id()
    usuario = model.Usuario.query.get(idUsuario)
    
    viajesPasajero = len(model.Pasajero.query.filter_by(id_usuario = idUsuario, id_estado_pasajero = 6).all())
    viajesConductor = len(model.Viaje.query.filter_by(id_conductor = idUsuario, id_estado_viaje = 2).all())

    edad = fper.calcular_edad(usuario.fecha_nacimiento)
    return render_template('perfil.html', edad = edad, viajesPasajero = viajesPasajero, viajesConductor = viajesConductor, usuario = usuario)

@usuario_bp.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def EditarPerfil():
    return True

@usuario_bp.route('/perfil/eliminar', methods=['GET', 'POST'])
@login_required
def EliminarCuenta():
    return True
