from app import db
from datetime import datetime
from sqlalchemy.orm import relationship

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
    pasajero = relationship('Pasajero', backref = 'viaje')

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
        return '<id {}>'.format(self.id)

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
        return '<id {}>'.format(self.id)

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
        return '<id {}>'.format(self.id)

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
        return '<id {}>'.format(self.id)

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
