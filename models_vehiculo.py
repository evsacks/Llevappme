from app import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Vehiculo(db.Model):
    __tablename__ = 'vehiculo'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    patente = db.Column(db.Integer, unique = False, nullable = False)
    cantidad_asientos = db.Column(db.String, unique = False, nullable = False)
    
    fecha_creacion = db.Column(db.DateTime, default = datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default = datetime.utcnow)

    tipo_vehiculo = db.Column(db.Integer, db.ForeignKey('tipo_vehiculo.id'), nullable = False)
    marca = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable = False)
    modelo = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable = False)
    color = db.Column(db.Integer, db.ForeignKey('color.id'), nullable = False)

    viaje =  relationship('Viaje', backref = 'vehiculo')
    conductor =  relationship('Conductor', backref = 'vehiculo')
    seguro_vehiculo =  relationship('SeguroVehiculo', backref = 'vehiculo')

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
        return '<id {}>'.format(self.id)

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
        return '<id {}>'.format(self.id)

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
        return '<id {}>'.format(self.id)

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

class Marca(db.Model):
    __tablename__ = 'marca'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(30), unique = True, nullable = False)
    
    vehiculo = relationship('Vehiculo', backref = 'marca')
    

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

class Modelo(db.Model):
    __tablename__ = 'modelo'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(30), unique = True, nullable = False)

    id_marca = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable = False)
    
    vehiculo = relationship('Vehiculo', backref = 'modelo')
    

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

class Color(db.Model):
    __tablename__ = 'color'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(30), unique = True, nullable = False)
    
    vehiculo = relationship('Vehiculo', backref = 'color')
    

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