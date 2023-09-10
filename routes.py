from app import app, login_manager
from app import maps

from Usuario.routes import usuario_bp
from Viaje.routes import viaje_bp
from Vehiculo.routes import vehiculo_bp

import models as model

from flask import Blueprint, render_template, url_for, redirect

#Blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(vehiculo_bp)
app.register_blueprint(viaje_bp)

@login_manager.user_loader
def CargarUsuario(idUsuario):
	return model.Usuario.query.get(idUsuario)

def formato_fecha(date):
    meses = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
              "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    dia = date.day
    mes = meses[date.month - 1]
    anio = date.year
    fecha = "{} {}, {}".format(dia, mes, anio)

    return fecha

def formato_hora(time):
    # Obtiene las horas y minutos del objeto time
    hora = time.hour
    minutos = time.minute

    # Determina si es AM o PM
    periodo = "AM"
    if hora >= 12:
        periodo = "PM"
        if hora > 12:
            hora -= 12

    # Formatea la hora en formato HH:MM AM/PM
    horario = "{:02d}:{:02d} {}".format(hora, minutos, periodo)

    return horario

app.jinja_env.globals.update(formato_fecha=formato_fecha)
app.jinja_env.globals.update(formato_hora=formato_hora)

#Home
@app.route('/', methods=['GET', 'POST'])
def Home():
    return redirect(url_for('usuario_bp.Login'))