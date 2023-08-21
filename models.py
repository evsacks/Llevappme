from app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# USUARIO 

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(), unique = False, nullable = False)
    apellido = db.Column(db.String(), unique = False, nullable = False)
    email = db.Column(db.String(), unique = True, nullable = False)
    contrasenia = db.Column(db.String(), unique = False, nullable = False)
    telefono = db.Column(db.Integer, unique = True, nullable = False)
    fecha_nacimiento = db.Column(db.DateTime, unique = False, nullable = False)
    fecha_creacion = db.Column(db.DateTime, default = datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default = datetime.utcnow)

    id_tipo_usuario = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id'), nullable = False)
    id_estado_usuario = db.Column(db.Integer, db.ForeignKey('estado_usuario.id'), nullable = False)

    pasajeros =  relationship('Pasajero', backref = 'usuario')
    conductores =  relationship('Conductor', backref = 'usuario')
    viajes =  relationship('Viaje', backref = 'usuario')

    def __init__(self, nombre, apellido, email, contrasenia, telefono, fecha_nacimiento, fecha_creacion, fecha_actualizacion, id_tipo_usuario, id_estado_usuario):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.contrasenia = generate_password_hash(contrasenia)
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion
        self.id_estado_usuario = id_estado_usuario
        self.id_tipo_usuario = id_tipo_usuario

    def __repr__(self):
        id = self.id
        nombre = self.nombre
        apellido = self.apellido
        email = self.email
        contrasenia = self.contrasenia
        telefono = self.telefono
        fecha_nacimiento = self.fecha_nacimiento
        fecha_creacion = self.fecha_creacion
        fecha_actualizacion = self.fecha_actualizacion
        id_estado_usuario = self.id_estado_usuario
        id_tipo_usuario = self.id_tipo_usuario
        usu = ('<Usuario(id={}, nombre={}, apellido={}, email={}, \
                         contrasenia={}, telefono={}, fecha nacimiento={}, fecha creacion={}, \
                         fecha actualizacion={}, estado usuario={}, tipo usuario={})>'
               .format(id, nombre, apellido, email, contrasenia, telefono,\
                       fecha_nacimiento, fecha_creacion, fecha_actualizacion, \
                       id_estado_usuario, id_tipo_usuario))
        return usu

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'contrasenia': self.contrasenia,
            'telefono': self.telefono,
            'fecha_nacimiento': self.fecha_nacimiento,
            'fecha_creacion': self.fecha_creacion,
            'fecha_actualizacion': self.fecha_actualizacion,
            'id_estado_usuario': self.id_estado_usuario,
            'id_tipo_usuario': self.id_tipo_usuario
    }

    @classmethod
    def find_by_email(cls, mail):
        return cls.query.filter_by(email=mail).first()
    
    def set_contrasenia(self, contrasenia):
        self.contrasenia = generate_password_hash(contrasenia)
    
    def validar_contrasenia(self, contrasenia):
        return check_password_hash(self.contrasenia, contrasenia)
    
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


# VIAJE

class Viaje(db.Model):
    __tablename__ = 'viaje'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    asientos_disponibles = db.Column(db.Integer, unique = False, nullable = False)
    distancia = db.Column(db.Integer, unique = False, nullable = False)

    direccion_inicial = db.Column(db.String, unique = False, nullable = False)
    direccion_final = db.Column(db.String, unique = False, nullable = False)

    latitud_inicial = db.Column(db.String, unique = False, nullable = False)
    latitud_final = db.Column(db.String, unique = False, nullable = False)
    longitud_inicial = db.Column(db.String, unique = False, nullable = False)
    longitud_final = db.Column(db.String, unique = False, nullable = False)
    
    fecha_inicio = db.Column(db.DateTime, unique = False, nullable = False)
    fecha_inicio_real = db.Column(db.DateTime, unique = False, nullable = True)
    fecha_final = db.Column(db.Date, unique = False, nullable = False)
    fecha_final_real = db.Column(db.DateTime, unique = False, nullable = True)

    id_conductor = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)
    id_vehiculo = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), nullable = True)
    id_estado_viaje = db.Column(db.Integer, db.ForeignKey('estado_viaje.id'), nullable = False)

    tracking = relationship('Tracking', backref = 'viaje')
    pasajeros = relationship('Pasajero', backref = 'viaje')

    def __init__(self, asientos_disponibles, distancia, direccion_inicial, direccion_final, latitud_inicial, latitud_final, longitud_inicial, longitud_final, fecha_inicio, fecha_inicio_real, fecha_final, fecha_final_real, id_conductor, id_vehiculo, id_estado_viaje):
        self.asientos_disponibles = asientos_disponibles
        self.distancia = distancia
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
        self.id_conductor = id_conductor
        self.id_vehiculo = id_vehiculo
        self.id_estado_viaje = id_estado_viaje

    def __repr__(self):
        asientos_disponibles = self.asientos_disponibles
        distancia = self.distancia
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
        id_conductor = self.id_conductor
        id_vehiculo = self.id_vehiculo
        id_estado_viaje = self.id_estado_viaje
        viaje = '<Viaje(id={}, cantidad pasajeros={}, distancia={}, \
                        direccion inicial={}, direccion final={}, latitud inicial={}, \
                        latitud final={}, longitud inicial={}, longitud final={}, \
                        fecha inicio={}, fecha inicio real={}, fecha final={}, \
                        fecha final real={}, conductor={}, vehiculo={}, estado viaje={})>'\
                .format(id,asientos_disponibles,distancia,direccion_inicial,direccion_final,\
                        latitud_inicial,latitud_final,longitud_inicial,longitud_final,fecha_inicio,\
                        fecha_inicio_real,fecha_final,fecha_final_real,id_conductor,id_vehiculo, id_estado_viaje)
        return viaje

    def serialize(self):
        return {
            'asientos_disponibles': self.asientos_disponibles,
            'distancia': self.distancia,
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
            'id_conductor': self.id_conductor,
            'id_vehiculo': self.id_vehiculo,
            'id_estado_viaje': self.id_estado_viaje
    }
    
    @classmethod
    def viajes_pendientes_usuario(cls,idUsuario):
        viajes = cls.query.filter((cls.id_conductor==idUsuario) & \
                                  (cls.id_estado_viaje == 3)).all() 
        
        return viajes
    
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
    id_estado_pasajero = db.Column(db.Integer, db.ForeignKey('estado_pasajero.id'), nullable = False)

    def __init__(self, fecha_solicitud, fecha_actualizacion, id_usuario, id_viaje, id_estado_pasajero):
        self.fecha_solicitud = fecha_solicitud
        self.fecha_actualizacion = fecha_actualizacion
        self.id_usuario = id_usuario
        self.id_viaje = id_viaje
        self.id_estado_pasajero = id_estado_pasajero

    def __repr__(self):
        id = self.id
        fecha_solicitud = self.fecha_solicitud
        fecha_actualizacion = self.fecha_actualizacion
        id_usuario = self.id_usuario
        id_viaje = self.id_viaje
        id_estado_pasajero = self.id_estado_pasajero
        pasajero = '<Tracking(id={}, fecha solicitud={}, fecha actualizacion={}, \
                              pasajero={}, viaje={}, estado pasajero={})>'\
                    .format(id,fecha_solicitud, fecha_actualizacion,id_usuario,id_viaje,id_estado_pasajero)
        return pasajero

    def serialize(self):
        return {
            'id': self.id,
            'fecha_solicitud': self.fecha_solicitud,
            'fecha_actualizacion': self.fecha_actualizacion,
            'id_usuario': self.id_usuario,
            'id_viaje': self.id_viaje,
            'id_estado_pasajero': self.id_estado_pasajero
    }

    @classmethod
    def viajes_activos_pasajero(cls,idUsuario):
        pasajeros = cls.query.filter((cls.id_usuario==idUsuario) & \
                                  ((cls.id_estado_pasajero == 1) | \
                                   (cls.id_estado_pasajero == 2))).all() 
        viajes = [ Viaje.query.get(idViaje) for idViaje in pasajeros]
        return viajes
    
    @classmethod
    def solicitud_activa(cls,idUsuario,idViaje):
        pasajeros = cls.query.filter((cls.id_usuario == idUsuario)  & \
                                     (cls.id_viaje == idViaje)      & \
                                    ((cls.id_estado_pasajero == 1)  | \
                                     (cls.id_estado_pasajero == 2))).first() 
        return pasajeros

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
    
    pasajeros = relationship('Pasajero', backref = 'estado')
    

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
    
    viajes = relationship('Viaje', backref = 'estado')
    

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
    cantidad_asientos = db.Column(db.Integer, unique = False, nullable = False)
    descripcion = db.Column(db.String, unique = False, nullable = False)
    
    fecha_creacion = db.Column(db.DateTime, default = datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default = datetime.utcnow)

    viajes =  relationship('Viaje', backref = 'vehiculo')
    conductores =  relationship('Conductor', backref = 'vehiculo')

    def __init__(self, patente, cantidad_asientos, descripcion, fecha_creacion, fecha_actualizacion):
        self.patente = patente
        self.cantidad_asientos = cantidad_asientos
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion

    def __repr__(self):
        id = self.id,
        patente = self.patente
        cantidad_asientos = self.cantidad_asientos
        descripcion = self.descripcion
        fecha_creacion = self.fecha_creacion
        fecha_actualizacion = self.fecha_actualizacion
        vehiculo = '<Vehiculo(id={},patente={}, cantidad asientos={}, descripcion={}\
                             fecha creacion={}, fecha actualizacion={})>'\
                   .format(id,patente, cantidad_asientos, descripcion, fecha_creacion, fecha_actualizacion)
        return vehiculo

    def serialize(self):
        return {
            'patente': self.patente,
            'cantidad_asientos': self.cantidad_asientos,
            'descripcion':self.descripcion,
            'fecha_creacion': self.fecha_creacion,
            'fecha_actualizacion': self.fecha_actualizacion
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

    def __init__(self, id_usuario, id_vehiculo):
        self.id_usuario = id_usuario
        self.id_vehiculo = id_vehiculo

    def __repr__(self):
        id = self.id
        id_usuario = self.id_usuario
        id_vehiculo = self.id_vehiculo
        conductor = '<Conductor(id={}, conductor={}, vehiculo={})>'\
                    .format(id, id_usuario, id_vehiculo)
        return conductor

    def serialize(self):
        return {
            'id': self.id,
            'id_usuario': self.id_usuario,
            'id_vehiculo': self.id_vehiculo
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
