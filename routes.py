from app import app, login_manager
from app import maps

from Usuario.routes import usuario_bp
from Viaje.routes import viaje_bp
from Vehiculo.routes import vehiculo_bp

import models as model

from flask import Blueprint, render_template, url_for, redirect
from Viaje.functions.f_AccionesConductor import viaje_en_curso_como_conductor, viaje_en_curso_como_pasajero
from Usuario.functions.f_AccionesUsuario import esConductor
from datetime import datetime, timedelta

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

def formato_fecha_corta(date):
    fecha = date.strftime("%d/%m/%Y")
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

def viaje_en_curso(idUsuario):
    conductor = viaje_en_curso_como_conductor(idUsuario)
    pasajero = viaje_en_curso_como_pasajero(idUsuario)
    print("conductor: ", conductor, "Pasajero: ", pasajero)
    if conductor:
        return conductor
    elif pasajero:
        return pasajero
    else:
        return False

def proximos_al_viaje(fecha_objetivo):
    # Obtenemos la fecha y hora actual
    fecha_actual = datetime.now()

    # Calculamos la diferencia entre la fecha objetivo y la fecha actual
    diferencia = fecha_objetivo - fecha_actual

    # Creamos un objeto timedelta con 15 minutos
    quince_minutos = timedelta(minutes=15)
    print("Diferencia: ", diferencia, "Comparacion: ", diferencia <= quince_minutos)
    # Comparamos la diferencia con los 15 minutos
    if diferencia <= quince_minutos:
        return True
    else:
        return False

def modo_conductor():
    return esConductor()
    

app.jinja_env.globals.update(formato_fecha=formato_fecha)
app.jinja_env.globals.update(formato_hora=formato_hora)
app.jinja_env.globals.update(formato_fecha_corta=formato_fecha_corta)
app.jinja_env.globals.update(viaje_en_curso=viaje_en_curso)
app.jinja_env.globals.update(proximos_al_viaje=proximos_al_viaje)
app.jinja_env.globals.update(modo_conductor=modo_conductor)

#Home
@app.route('/', methods=['GET', 'POST'])
def Home():
    return redirect(url_for('usuario_bp.Login'))