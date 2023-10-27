from datetime import date

def calcular_edad(fecha_nacimiento):
    # Obtiene la fecha actual
    fecha_actual = date.today()

    # Calcula la diferencia entre la fecha actual y la fecha de nacimiento
    edad = fecha_actual.year - fecha_nacimiento.year

    # Verifica si ya ha pasado el cumpleaños de la persona en el año actual
    if fecha_nacimiento.month > fecha_actual.month or (fecha_nacimiento.month == fecha_actual.month and fecha_nacimiento.day > fecha_actual.day):
        edad -= 1

    return edad