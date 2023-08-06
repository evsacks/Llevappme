from app import db
from datetime import datetime
from sqlalchemy.orm import relationship


# USUARIO 

class Usuario(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(), unique = False, nullable = False)
    apellido = db.Column(db.String(), unique = False, nullable = False)
    email = db.Column(db.String(), unique = True, nullable = False)
    contrasenia = db.Column(db.String(), unique = False, nullable = False)
    telefono = db.Column(db.Integer, unique = True, nullable = False)
    dni = db.Column(db.Integer, unique = True, nullable = False)
    fecha_nacimiento = db.Column(db.DateTime, unique = False, nullable = False)
    fecha_creacion = db.Column(db.DateTime, default = datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default = datetime.utcnow)

    tipo = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id'), nullable = False)
    estado = db.Column(db.Integer, db.ForeignKey('estado_usuario.id'), nullable = False)

    licencias_conducir =  relationship('LicenciaConducir', backref = 'usuario')
    pasajeros =  relationship('Pasajero', backref = 'usuario')
    conductores =  relationship('Conductor', backref = 'usuario')
    viajes =  relationship('Viaje', backref = 'usuario')

    def __init__(self, nombre, apellido, email, contrasenia, telefono, dni, fecha_nacimiento, fecha_creacion, fecha_actualizacion, tipo, estado):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.contrasenia = contrasenia
        self.telefono = telefono
        self.dni = dni
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion
        self.estado = estado
        self.tipo = tipo

    def __repr__(self):
        id = self.id
        nombre = self.nombre
        apellido = self.apellido
        email = self.email
        contrasenia = self.contrasenia
        telefono = self.telefono
        dni = self.dni
        fecha_nacimiento = self.fecha_nacimiento
        fecha_creacion = self.fecha_creacion
        fecha_actualizacion = self.fecha_actualizacion
        estado = self.estado
        tipo = self.tipo
        usu = ('<Usuario(id={}, nombre={}, apellido={}, email={}, \
                         contrasenia={}, telefono={}, dni={}, \
                         fecha nacimiento={}, fecha creacion={}, \
                         fecha actualizacion={}, estado={}, tipo={})>'
               .format(id, nombre, apellido, email, contrasenia, telefono,\
                       dni, fecha_nacimiento, fecha_creacion, fecha_actualizacion, estado, tipo))
        return usu

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'contrasenia': self.contrasenia,
            'telefono': self.telefono,
            'dni': self.dni,
            'fecha_nacimiento': self.fecha_nacimiento,
            'fecha_creacion': self.fecha_creacion,
            'fecha_actualizacion': self.fecha_actualizacion,
            'estado': self.estado,
            'tipo': self.tipo
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class EstadoUsuario(db.Model):
    __tablename__ = 'estado_usuario'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(30), unique = True, nullable = False)
    usuarios = relationship('Usuario', backref = 'estado_usuario')
    

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        id = self.id,
        descripcion = self.descripcion
        est_usu = '<Estado Usuario(id={}, descripcion={})>'.format(id,descripcion)
        return est_usu

    def serialize(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class TipoUsuario(db.Model):
    __tablename__ = 'tipo_usuario'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(3), unique = True, nullable = False)
    descripcion = db.Column(db.String(30), unique = True, nullable = False)
    usuarios = relationship('Usuario', backref = 'tipo_usuario')
    

    def __init__(self, codigo, descripcion):
        self.codigo = codigo
        self.descripcion = descripcion

    def __repr__(self):
        id = self.id,
        codigo = self.codigo,
        descripcion = self.descripcion
        tipo_usu = '<Tipo Usuario(id={}, codigo={}, descripcion={})>'.format(id,descripcion)
        return tipo_usu

    def serialize(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'descripcion': self.descripcion
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class LicenciaConducir(db.Model):
    __tablename__ = 'licencia_conducir'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_licencia = db.Column(db.Integer, unique = True, nullable = False)
    fecha_otorgamiento = db.Column(db.DateTime, unique = False, nullable = False)
    fecha_vencimiento = db.Column(db.DateTime, unique = False, nullable = False)
    imagen = db.Column(db.String(30), unique = True, nullable = False)
    
    id_conductor = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)
    

    def __init__(self, numero_licencia, fecha_otorgamiento, fecha_vencimiento, imagen, id_conductor):
        self.numero_licencia = numero_licencia
        self.fecha_otorgamiento = fecha_otorgamiento
        self.fecha_vencimiento = fecha_vencimiento
        self.imagen = imagen
        self.id_conductor = id_conductor

    def __repr__(self):
        id = self.id
        numero_licencia = self.numero_licencia
        fecha_otorgamiento = self.fecha_otorgamiento
        fecha_vencimiento = self.fecha_vencimiento
        imagen = self.imagen
        id_conductor = self.id_conductor
        lic_conduc = '<Licencia Conducir(id={}, numero licencia={}, fecha otorgamiento={}, \
                                         fecha vencimiento={}, imagen={}, conductor={})>'\
                      .format(id,numero_licencia, fecha_otorgamiento, fecha_vencimiento, imagen, id_conductor)
        return lic_conduc

    def serialize(self):
        return {
            'id': self.id,
            'numero_licencia': self.numero_licencia,
            'fecha_otorgamiento': self.fecha_otorgamiento,
            'fecha_vencimiento': self.fecha_vencimiento,
            'imagen': self.imagen,
            'id_conductor': self.id_conductor
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


# VIAJE

class Viaje(db.Model):
    __tablename__ = 'viaje'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    cantidad_pasajeros = db.Column(db.Integer, unique = False, nullable = False)
    distancia = db.Column(db.Integer, unique = False, nullable = False)
    costo_total = db.Column(db.Float, unique = False, nullable = False)

    direccion_inicial = db.Column(db.String, unique = False, nullable = False)
    direccion_final = db.Column(db.String, unique = False, nullable = False)

    latitud_inicial = db.Column(db.String, unique = False, nullable = False)
    latitud_final = db.Column(db.String, unique = True, nullable = False)
    longitud_inicial = db.Column(db.String, unique = False, nullable = False)
    longitud_final = db.Column(db.String, unique = True, nullable = False)
    
    fecha_inicio = db.Column(db.DateTime, unique = False, nullable = False)
    fecha_inicio_real = db.Column(db.DateTime, unique = False, nullable = False)
    fecha_final = db.Column(db.DateTime, unique = False, nullable = False)
    fecha_final_real = db.Column(db.DateTime, unique = False, nullable = False)

    conductor = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)
    vehiculo = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), nullable = False)

    tracking = relationship('Tracking', backref = 'viaje')
    pasajeros = relationship('Pasajero', backref = 'viaje')

    def __init__(self, cantidad_pasajeros, distancia, costo_total, direccion_inicial, direccion_final, latitud_inicial, latitud_final, longitud_inicial, longitud_final, fecha_inicio, fecha_inicio_real, fecha_final, fecha_final_real, conductor, vehiculo):
        self.cantidad_pasajeros = cantidad_pasajeros
        self.distancia = distancia
        self.costo_total = costo_total
        self.direccion_inicial = direccion_inicial
        self.direccion_final = direccion_final
        self.latitud_inicial = latitud_inicial
        self.latitud_final = latitud_final
        self.longitud_inicial = longitud_inicial
        self.longitud_final = longitud_final
        self.fecha_inicio = fecha_inicio
        self.fecha_inicio_real = fecha_inicio_real
        self.fecha_final = fecha_final
        self.fecha_final_real = fecha_final_real
        self.conductor = conductor
        self.vehiculo = vehiculo

    def __repr__(self):
        cantidad_pasajeros = self.cantidad_pasajeros
        distancia = self.distancia
        costo_total = self.costo_total
        direccion_inicial = self.direccion_inicial
        direccion_final = self.direccion_final
        latitud_inicial = self.latitud_inicial
        latitud_final = self.latitud_final
        longitud_inicial = self.longitud_inicial
        longitud_final = self.longitud_final
        fecha_inicio = self.fecha_inicio
        fecha_inicio_real = self.fecha_inicio_real
        fecha_final = self.fecha_final
        fecha_final_real = self.fecha_final_real
        conductor = self.conductor
        vehiculo = self.vehiculo
        viaje = '<Viaje(id={}, cantidad pasajeros={}, distancia={}, costo total={}\
                        direccion inicial={}, direccion final={}, latitud inicial={}, \
                        latitud final={}, longitud inicial={}, longitud final={}, \
                        fecha inicio={}, fecha inicio real={}, fecha final={}, \
                        fecha final real={}, conductor={}, vehiculo={})>'\
                .format(id,cantidad_pasajeros,distancia,costo_total,direccion_inicial,direccion_final,\
                        latitud_inicial,latitud_final,longitud_inicial,longitud_final,fecha_inicio,\
                        fecha_inicio_real,fecha_final,fecha_final_real,conductor,vehiculo)
        return viaje

    def serialize(self):
        return {
            'cantidad_pasajeros': self.cantidad_pasajeros,
            'distancia': self.distancia,
            'costo_total': self.costo_total,
            'direccion_inicial': self.direccion_inicial,
            'direccion_final': self.direccion_final,
            'latitud_inicial': self.latitud_inicial,
            'latitud_final': self.latitud_final,
            'longitud_inicial': self.longitud_inicial,
            'longitud_final': self.longitud_final,
            'fecha_inicio': self.fecha_inicio,
            'fecha_inicio_real': self.fecha_inicio_real,
            'fecha_final': self.fecha_final,
            'fecha_final_real': self.fecha_final_real,
            'conductor': self.conductor,
            'vehiculo': self.vehiculo
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Tracking(db.Model):
    __tablename__ = 'tracking'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    latitud = db.Column(db.String, unique = False, nullable = False)
    longitud = db.Column(db.String, unique = False, nullable = False)
    fecha = db.Column(db.DateTime, default = datetime.utcnow)

    id_viaje = db.Column(db.Integer, db.ForeignKey('viaje.id'), nullable = False)
    

    def __init__(self, latitud, longitud, fecha, id_viaje):
        self.latitud = latitud
        self.longitud = longitud
        self.fecha = fecha
        self.id_viaje = id_viaje

    def __repr__(self):
        id = self.id
        latitud = self.latitud
        longitud = self.longitud
        fecha = self.fecha
        id_viaje = self.id_viaje
        tracking = '<Tracking(id={}, latitud={}, longitud={}, fecha={}, viaje={})>'\
                    .format(id,latitud, longitud,fecha,id_viaje)
        return tracking

    def serialize(self):
        return {
            'id': self.id,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'fecha': self.fecha,
            'id_viaje': self.id_viaje
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Pasajero(db.Model):
    __tablename__ = 'pasajero'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha_solicitud = db.Column(db.DateTime, default = datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default = datetime.utcnow)
    
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)
    id_viaje = db.Column(db.Integer, db.ForeignKey('viaje.id'), nullable = False)
    estado_pasajero = db.Column(db.Integer, db.ForeignKey('estado_pasajero.id'), nullable = False)

    def __init__(self, fecha_solicitud, fecha_actualizacion, id_usuario, id_viaje, estado_pasajero):
        self.fecha_solicitud = fecha_solicitud
        self.fecha_actualizacion = fecha_actualizacion
        self.id_usuario = id_usuario
        self.id_viaje = id_viaje
        self.estado_pasajero = estado_pasajero

    def __repr__(self):
        id = self.id
        fecha_solicitud = self.fecha_solicitud
        fecha_actualizacion = self.fecha_actualizacion
        id_usuario = self.id_usuario
        id_viaje = self.id_viaje
        estado_pasajero = self.estado_pasajero
        pasajero = '<Tracking(id={}, fecha solicitud={}, fecha actualizacion={}, \
                              pasajero={}, viaje={}, estado pasajero={})>'\
                    .format(id,fecha_solicitud, fecha_actualizacion,id_usuario,id_viaje,estado_pasajero)
        return pasajero

    def serialize(self):
        return {
            'id': self.id,
            'fecha_solicitud': self.fecha_solicitud,
            'fecha_actualizacion': self.fecha_actualizacion,
            'id_usuario': self.id_usuario,
            'id_viaje': self.id_viaje,
            'estado_pasajero': self.estado_pasajero
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class EstadoPasajero(db.Model):
    __tablename__ = 'estado_pasajero'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(30), unique = True, nullable = False)
    
    pasajeros = relationship('Pasajero', backref = 'estado_pasajero')
    

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        id = self.id,
        descripcion = self.descripcion
        est_pasajero = '<Estado Pasajero(id={}, descripcion={})>'.format(id,descripcion)
        return est_pasajero

    def serialize(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class EstadoViaje(db.Model):
    __tablename__ = 'estado_viaje'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(30), unique = True, nullable = False)
    
    viajes = relationship('Viaje', backref = 'estado_viaje')
    

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        id = self.id,
        descripcion = self.descripcion
        est_viaje = '<Estado Viaje(id={}, descripcion={})>'.format(id,descripcion)
        return est_viaje

    def serialize(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

# VEHICULO

class Vehiculo(db.Model):
    __tablename__ = 'vehiculo'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    patente = db.Column(db.String, unique = False, nullable = False)
    cantidad_asientos = db.Column(db.String, unique = False, nullable = False)
    
    fecha_creacion = db.Column(db.DateTime, default = datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default = datetime.utcnow)

    tipo_vehiculo = db.Column(db.Integer, db.ForeignKey('tipo_vehiculo.id'), nullable = False)
    marca = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable = False)
    modelo = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable = False)
    color = db.Column(db.Integer, db.ForeignKey('color.id'), nullable = False)

    viajes =  relationship('Viaje', backref = 'vehiculo')
    conductores =  relationship('Conductor', backref = 'vehiculo')
    seguros_vehiculo =  relationship('SeguroVehiculo', backref = 'vehiculo')

    def __init__(self, patente, cantidad_asientos, fecha_creacion, fecha_actualizacion, tipo_vehiculo, marca, modelo, color):
        self.patente = patente
        self.cantidad_asientos = cantidad_asientos
        self.fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion
        self.tipo_vehiculo = tipo_vehiculo
        self.marca = marca
        self.modelo = modelo
        self.color = color

    def __repr__(self):
        id = self.id,
        patente = self.patente
        cantidad_asientos = self.cantidad_asientos
        fecha_creacion = self.fecha_creacion
        fecha_actualizacion = self.fecha_actualizacion
        tipo_vehiculo = self.tipo_vehiculo
        marca = self.marca
        modelo = self.modelo
        color = self.color
        vehiculo = '<Vehiculo(id={},patente={}, cantidad asientos={}, fecha creacion={}, \
                             fecha actualizacion={}, tipo vehiculo={}, marca={}, modelo={}, \
                             color={})>'\
                   .format(id,patente, cantidad_asientos, fecha_creacion, fecha_actualizacion, \
                          tipo_vehiculo, marca, modelo, color)
        return vehiculo

    def serialize(self):
        return {
            'patente': self.patente,
            'cantidad_asientos': self.cantidad_asientos,
            'fecha_creacion': self.fecha_creacion,
            'fecha_actualizacion': self.fecha_actualizacion,
            'tipo_vehiculo': self.tipo_vehiculo,
            'marca': self.marca,
            'modelo': self.modelo,
            'color': self.color
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Conductor(db.Model):
    __tablename__ = 'conductor'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)
    id_vehiculo = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), nullable = False)
    cedula = db.Column(db.Integer, db.ForeignKey('cedula_conductor.id'), nullable = False)
    

    def __init__(self, id_usuario, id_vehiculo, cedula):
        self.id_usuario = id_usuario
        self.id_vehiculo = id_vehiculo
        self.cedula = cedula

    def __repr__(self):
        id = self.id
        id_usuario = self.id_usuario
        id_vehiculo = self.id_vehiculo
        cedula = self.cedula
        conductor = '<Conductor(id={}, conductor={}, vehiculo={}, cedula={})>'\
                    .format(id, id_usuario, id_vehiculo, cedula)
        return conductor

    def serialize(self):
        return {
            'id': self.id,
            'id_usuario': self.id_usuario,
            'id_vehiculo': self.id_vehiculo,
            'cedula': self.cedula
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class CedulaConductor(db.Model):
    __tablename__ = 'cedula_conductor'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.String, unique = True, nullable = False)
    imagen = db.Column(db.String, unique = True, nullable = False)
    fecha_otorgamiento = db.Column(db.DateTime, unique = False, nullable = False)
    fecha_vencimiento = db.Column(db.DateTime, unique = False, nullable = False)
    
    tipo_cedula = db.Column(db.Integer, db.ForeignKey('tipo_cedula.id'), nullable = False)

    def __init__(self, numero, imagen, fecha_otorgamiento, fecha_vencimiento, tipo_cedula):
        self.numero = numero
        self.imagen = imagen
        self.fecha_otorgamiento = fecha_otorgamiento
        self.fecha_vencimiento = fecha_vencimiento
        self.tipo_cedula = tipo_cedula

    def __repr__(self):
        id = self.id
        numero = self.numero
        imagen = self.imagen
        fecha_otorgamiento = self.fecha_otorgamiento
        fecha_vencimiento = self.fecha_vencimiento
        tipo_cedula = self.tipo_cedula
        cedula_cond = '<Cedula(numero={}, imagen={}, fecha_otorgamiento={}, \
                        fecha_vencimiento={}, tipo_cedula={})>'\
                    .format(id, numero, imagen, fecha_otorgamiento, fecha_vencimiento, tipo_cedula)
        return cedula_cond

    def serialize(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'imagen': self.imagen,
            'fecha_otorgamiento': self.fecha_otorgamiento,
            'fecha_vencimiento': self.fecha_vencimiento,
            'tipo_cedula': self.tipo_cedula
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class TipoCedula(db.Model):
    __tablename__ = 'tipo_cedula'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(30), unique = True, nullable = False)
    
    cedula = relationship('CedulaConductor', backref = 'tipo_cedula')
    

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        id = self.id,
        descripcion = self.descripcion
        tipo_cedula = '<Tipo Cedula(id={}, descripcion={})>'.format(id,descripcion)
        return tipo_cedula

    def serialize(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class SeguroVehiculo(db.Model):
    __tablename__ = 'seguro_vehiculo'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.String, unique = True, nullable = False)
    imagen = db.Column(db.String, unique = True, nullable = False)
    fecha_otorgamiento = db.Column(db.DateTime, unique = False, nullable = False)
    fecha_vencimiento = db.Column(db.DateTime, unique = False, nullable = False)
    
    id_vehiculo = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), nullable = False)

    def __init__(self, numero, imagen, fecha_otorgamiento, fecha_vencimiento, id_vehiculo):
        self.numero = numero
        self.imagen = imagen
        self.fecha_otorgamiento = fecha_otorgamiento
        self.fecha_vencimiento = fecha_vencimiento
        self.id_vehiculo = id_vehiculo

    def __repr__(self):
        id = self.id
        numero = self.numero
        imagen = self.imagen
        fecha_otorgamiento = self.fecha_otorgamiento
        fecha_vencimiento = self.fecha_vencimiento
        id_vehiculo = self.id_vehiculo
        seguro_vehi = '<Seguro Vehiculo(id={}, numero={}, imagen={}, fecha otorgamiento={}, \
                        fecha vencimiento={}, vehiculo={})>'\
                      .format(id,numero, imagen, fecha_otorgamiento, fecha_vencimiento, id_vehiculo)
        return seguro_vehi

    def serialize(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'imagen': self.imagen,
            'fecha_otorgamiento': self.fecha_otorgamiento,
            'fecha_vencimiento': self.fecha_vencimiento,
            'id_vehiculo': self.id_vehiculo
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class TipoVehiculo(db.Model):
    __tablename__ = 'tipo_vehiculo'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(30), unique = True, nullable = False)
    
    vehiculo = relationship('Vehiculo', backref = 'tipo_vehiculo')
    

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        id = self.id,
        descripcion = self.descripcion
        tipo_vehi = '<Tipo Vehiculo(id={}, descripcion={})>'.format(id,descripcion)
        return tipo_vehi

    def serialize(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Marca(db.Model):
    __tablename__ = 'marca'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(30), unique = True, nullable = False)
    
    vehiculo = relationship('Vehiculo', backref = 'marca')
    

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        id = self.id,
        descripcion = self.descripcion
        marca = '<Marca(id={}, descripcion={})>'.format(id,descripcion)
        return marca

    def serialize(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Modelo(db.Model):
    __tablename__ = 'modelo'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(30), unique = False, nullable = False)

    id_marca = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable = False)
    
    vehiculos = relationship('Vehiculo', backref = 'modelo')
    

    def __init__(self, descripcion, id_marca):
        self.descripcion = descripcion
        self.id_marca = id_marca

    def __repr__(self):
        id = self.id,
        descripcion = self.descripcion
        id_marca = self.id_marca
        modelo = '<Modelo(id={}, descripcion={}, marca={})>'.format(id,descripcion,id_marca)
        return modelo

    def serialize(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'id_marca': self.id_marca
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Color(db.Model):
    __tablename__ = 'color'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(30), unique = True, nullable = False)
    
    vehiculos = relationship('Vehiculo', backref = 'color')
    

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        id = self.id,
        descripcion = self.descripcion
        color = '<Color(id={}, descripcion={})>'.format(id,descripcion)
        return color

    def serialize(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()