from app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#Hay que agregar el serializador a cada clase y eliminar serialize.
#Investigar la posibilidad de agregar services y separar las tablas de metodos de base de datos.
class SerializableMixin:
    def serialize(self):
        serialized_data = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            serialized_data[column.name] = value
        return serialized_data

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

    def __init__(self, nombre, apellido, email, contrasenia, telefono, fecha_nacimiento, fecha_creacion, fecha_actualizacion, id_tipo_usuario, id_estado_usuario):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.contrasenia = contrasenia
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
    
    @classmethod
    def find_by_telefono(cls, telefono):
        return cls.query.filter_by(telefono=telefono).first()

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

    def update_from_db():
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

    def update_from_db():
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
        tipo_usu = '<Tipo Usuario(id={}, codigo={}, descripcion={})>'.format(id,codigo,descripcion)
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

    def update_from_db():
        db.session.commit()

class Notificacion(db.Model):
    __tablename__ = 'notificacion'
    __table_args__ = {'extend_existing': True} 
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contenido = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Campos para relacionar la notificación con usuarios
    id_emisor = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_receptor = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
    # Agregar una columna para indicar si la notificación ha sido leída o no
    leida = db.Column(db.Boolean, default=False)
    
    def __init__(self, contenido, id_emisor, id_receptor):
        self.contenido = contenido
        self.id_emisor = id_emisor
        self.id_receptor = id_receptor

    def __repr__(self):
        id = self.id
        contenido = self.contenido
        fecha_creacion = self.fecha_creacion
        id_emisor = self.id_emisor
        id_receptor = self.id_receptor
        leida = self.leida
        notificacion = '<Notificacion(id={}, contenido={}, fecha creacion={}, emisor={}, receptor={}, leida = {})>'\
                .format(id,contenido, fecha_creacion,id_emisor,id_receptor,leida)
        return notificacion
    
    def serialize(self):
        return {
            'id': self.id,
            'contenido': self.contenido,
            'fecha_creacion': self.fecha_creacion,
            'id_emisor': self.id_emisor,
            'id_receptor': self.id_receptor,
            'leida': self.leida
        }
    
    def marcar_como_leida(self):
        self.leida = True
    
    def update_from_db():
        db.session.commit()
# VIAJE

class Viaje(db.Model):
    __tablename__ = 'viaje'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    asientos_disponibles = db.Column(db.Integer, unique = False, nullable = False)

    fecha_inicio = db.Column(db.DateTime, unique = False, nullable = False)
    fecha_inicio_real = db.Column(db.DateTime, unique = False, nullable = True)
    fecha_final = db.Column(db.Date, unique = False, nullable = False)
    fecha_final_real = db.Column(db.DateTime, unique = False, nullable = True)

    id_conductor = db.Column(db.Integer, db.ForeignKey('conductor.id'), nullable = False)
    id_estado_viaje = db.Column(db.Integer, db.ForeignKey('estado_viaje.id'), nullable = False)
    id_ubicacion = db.Column(db.Integer, db.ForeignKey('ubicacion.id'), nullable = False)
    id_adicional = db.Column(db.Integer, db.ForeignKey('adicional.id'), nullable = False)

    tracking = relationship('Tracking', backref = 'viaje')
    pasajeros = relationship('Pasajero', backref = 'viaje')

    def __init__(self, asientos_disponibles, fecha_inicio, fecha_inicio_real, fecha_final, fecha_final_real, id_conductor, id_estado_viaje, id_ubicacion, id_adicional):
        self.asientos_disponibles = asientos_disponibles
        self.fecha_inicio = fecha_inicio
        self.fecha_inicio_real = fecha_inicio_real
        self.fecha_final = fecha_final
        self.fecha_final_real = fecha_final_real
        self.id_conductor = id_conductor
        self.id_estado_viaje = id_estado_viaje
        self.id_ubicacion = id_ubicacion
        self.id_adicional = id_adicional

    def __repr__(self):
        id = self.id
        asientos_disponibles = self.asientos_disponibles
        fecha_inicio = self.fecha_inicio
        fecha_inicio_real = self.fecha_inicio_real
        fecha_final = self.fecha_final
        fecha_final_real = self.fecha_final_real
        id_conductor = self.id_conductor
        id_estado_viaje = self.id_estado_viaje
        id_ubicacion = self.id_ubicacion
        id_adicional = self.id_adicional
        viaje = '<Viaje(id={}, cantidad pasajeros={}, fecha inicio={}, fecha inicio real={}, fecha final={}, \
                        fecha final real={}, conductor={}, estado viaje={}, ubicacion={}, adicional = {})>'\
                .format(id,asientos_disponibles,fecha_inicio,\
                        fecha_inicio_real,fecha_final,fecha_final_real,\
                        id_conductor, id_estado_viaje, id_ubicacion, id_adicional)
        return viaje

    def serialize(self):
        return {
            'id': self.id,
            'asientos_disponibles': self.asientos_disponibles,
            'fecha_inicio': self.fecha_inicio,
            'fecha_inicio_real': self.fecha_inicio_real,
            'fecha_final': self.fecha_final,
            'fecha_final_real': self.fecha_final_real,
            'id_conductor': self.id_conductor,
            'id_estado_viaje': self.id_estado_viaje,
            'id_ubicacion': self.id_ubicacion,
            'id_adicional': self.id_adicional
    }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_from_db():
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

    def update_from_db():
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
        pasajero = '<Pasajero(id={}, fecha solicitud={}, fecha actualizacion={}, \
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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    def update_from_db():
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

    def update_from_db():
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

    def update_from_db():
        db.session.commit()

class Ubicacion(db.Model):
    __tablename__ = 'ubicacion'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    direccion_inicial = db.Column(db.String, unique = False, nullable = False)
    direccion_final = db.Column(db.String, unique = False, nullable = False)

    latitud_inicial = db.Column(db.String, unique = False, nullable = False)
    latitud_final = db.Column(db.String, unique = False, nullable = False)
    longitud_inicial = db.Column(db.String, unique = False, nullable = False)
    longitud_final = db.Column(db.String, unique = False, nullable = False)

    viajes = relationship('Viaje', backref = 'ubicacion')

    def __init__(self, direccion_inicial, direccion_final, latitud_inicial, latitud_final, longitud_inicial, longitud_final):
        self.direccion_inicial = direccion_inicial
        self.direccion_final = direccion_final
        self.latitud_inicial = latitud_inicial
        self.latitud_final = latitud_final
        self.longitud_inicial = longitud_inicial
        self.longitud_final = longitud_final

    def __repr__(self):
        id = self.id
        direccion_inicial = self.direccion_inicial
        direccion_final = self.direccion_final
        latitud_inicial = self.latitud_inicial
        latitud_final = self.latitud_final
        longitud_inicial = self.longitud_inicial
        longitud_final = self.longitud_final
        ubicacion = '<Ubicacion(id={}, direccion inicial={}, direccion final={}, \
                                latitud inicial={}, latitud final={}, \
                                longitud inicial={}, longitud final={})>' \
                    .format(id,direccion_inicial,direccion_final,latitud_inicial,latitud_final,longitud_inicial,longitud_final)
        return ubicacion

    def serialize(self):
        return {
            'id': self.id,
            'direccion_inicial': self.direccion_inicial,
            'direccion_final': self.direccion_final,
            'latitud_inicial': self.latitud_inicial,
            'latitud_final': self.latitud_final,
            'longitud_inicial': self.longitud_inicial,
            'longitud_final': self.longitud_final,
    }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
   
    def update_from_db():
        db.session.commit()

class Adicional(db.Model):
    __tablename__ = 'adicional'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mascota = db.Column(db.Boolean, unique = False, nullable = False)
    equipaje = db.Column(db.Boolean, unique = False, nullable = False)
    alimentos = db.Column(db.Boolean, unique = False, nullable = False)

    viajes = relationship('Viaje', backref = 'adicional')

    def __init__(self, mascota, equipaje, alimentos):
        self.mascota = mascota
        self.equipaje = equipaje
        self.alimentos = alimentos

    def __repr__(self):
        id = self.id
        mascota = self.mascota
        equipaje = self.equipaje
        alimentos = self.alimentos
        adicional = '<Adicional_viaje(id={}, mascota={}, equipaje={}, alimentos={})>' \
                    .format(id,mascota,equipaje,alimentos)
        return adicional

    def serialize(self):
        return {
            'id': self.id,
            'mascota': self.mascota,
            'equipaje': self.equipaje,
            'alimentos': self.alimentos
    }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_from_db():
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

    conductores =  relationship('Conductor', backref = 'vehiculo')
    
    id_estado_vehiculo = db.Column(db.Integer, db.ForeignKey('estado_vehiculo.id'), nullable = False)

    def __init__(self, patente, cantidad_asientos, descripcion, fecha_creacion, fecha_actualizacion, id_estado_vehiculo):
        self.patente = patente
        self.cantidad_asientos = cantidad_asientos
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion
        self.fecha_actualizacion = fecha_actualizacion
        self.id_estado_vehiculo = 1


    def __repr__(self):
        id = self.id,
        patente = self.patente
        cantidad_asientos = self.cantidad_asientos
        descripcion = self.descripcion
        fecha_creacion = self.fecha_creacion
        fecha_actualizacion = self.fecha_actualizacion
        estado = self.id_estado_vehiculo
        vehiculo = '<Vehiculo(id={},patente={}, cantidad asientos={}, descripcion={}\
                             fecha creacion={}, fecha actualizacion={}, estado={})>'\
                   .format(id,patente, cantidad_asientos, descripcion, fecha_creacion, fecha_actualizacion,estado)
        return vehiculo

    def serialize(self):
        return {
            'id': self.id,
            'patente': self.patente,
            'cantidad_asientos': self.cantidad_asientos,
            'descripcion':self.descripcion,
            'fecha_creacion': self.fecha_creacion,
            'fecha_actualizacion': self.fecha_actualizacion,
            'estado_vehiculo':self.id_estado_vehiculo
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    def update_from_db():
        db.session.commit()

class EstadoVehiculo(db.Model):
    __tablename__ = 'estado_vehiculo'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(30), unique = True, nullable = False)
    vehiculos = relationship('Vehiculo', backref = 'estado_vehiculo')
    

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        id = self.id,
        descripcion = self.descripcion
        est_usu = '<Estado Vehiculo(id={}, descripcion={})>'.format(id,descripcion)
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

    def update_from_db():
        db.session.commit()

class Conductor(db.Model):
    __tablename__ = 'conductor'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)
    id_vehiculo = db.Column(db.Integer, db.ForeignKey('vehiculo.id'), nullable = False)

    viajes =  relationship('Viaje', backref = 'conductor')

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
    def update_from_db():
        db.session.commit()