from flask import Blueprint, render_template, redirect,url_for,flash
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime, timedelta
from authentication import auth
import models as model
import Usuario.forms as formulario
import Usuario.functions.f_perfil as fper

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/usuario', template_folder='templates', static_folder='static')


@usuario_bp.route('/registro', methods=['GET', 'POST'])
def Registro():
    if current_user.is_authenticated:
        return redirect(url_for('viaje_bp.BuscarViaje'))
    
    form = formulario.RegistroUsuario()

    if form.validate_on_submit():

        nombre= form.nombreUsuario.data
        apellido = form.apellidoUsuario.data
        email = form.email.data.strip()
        telefono = form.telefono.data
        fecha_nacimiento = form.fecha_nacimiento.data
        passw = form.password.data

        usuario_email = model.Usuario.find_by_email(email)
        usuario_telefono = model.Usuario.find_by_telefono(telefono)

        if usuario_email:
            flash("El email especificado ya esta en uso.")
            return render_template('registro.html', form=form)
        elif usuario_telefono:
            flash("El número de teléfono especificado ya esta en uso.")
            return render_template('registro.html', form=form)
        else:
            nuevoUsuario_firebase = auth.create_user_with_email_and_password(email, passw)
            print(nuevoUsuario_firebase)
            nuevoUsuario = model.Usuario(
                nombre=nombre,
                apellido=apellido,
                email=email,
                contrasenia=nuevoUsuario_firebase['idToken'],
                telefono=telefono,
                fecha_nacimiento=fecha_nacimiento,
                fecha_actualizacion=datetime.now(),
                fecha_creacion= datetime.now(),
                id_tipo_usuario=1,
                id_estado_usuario=1
            )
            model.Usuario.save_to_db(nuevoUsuario)
            if model.Usuario.query.get(nuevoUsuario.id):
                flash("Usuario creado exitosamente, complete sus credenciales para ingresar.")
                return redirect(url_for('usuario_bp.Login'))
            else:
                flash("Hubo un error al crear la cuenta, vuelve a intentarlo más tarde.")
                return render_template('registro.html', form=form)
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
            inicio = auth.sign_in_with_email_and_password(email, passw)
            if inicio:
                login_user(usuario)
                return redirect(url_for('viaje_bp.BuscarViaje'))
            else: 
                flash("La contraseña ingresada es incorrecta")
                return redirect(url_for('usuario_bp.Login'))
        else: 
            flash("El usuario ingresado es incorrecto")
            return redirect(url_for('usuario_bp.Login'))
    return render_template('login.html', form=form)

@usuario_bp.route('/reset/contrasenia', methods=['GET', 'POST'])
def ResetearContrasenia():
    if current_user.is_authenticated:
        return redirect(url_for('viaje_bp.BuscarViaje'))

    form = formulario.ReseteoContrasenia()

    if form.validate_on_submit():
        email = form.emailUsuario.data.strip()
        try:
            auth.send_password_reset_email(email)
            flash('Te enviamos un email a la cuenta de correo para que puedas resetear tu contraseña.')
            return redirect(url_for('usuario_bp.Login'))
        except:
            flash('El correo ingresado no pertenece a una cuenta existente.')
            return redirect(url_for('usuario_bp.ResetearContrasenia'))
    return render_template('reseteoContrasenia.html', form=form)

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
