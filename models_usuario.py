from app import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Usuario(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(), unique = False, nullable = False)
    apellido = db.Column(db.String(), unique = False, nullable = False)
    email = db.Column(db.String(), unique = True, nullable = False)
    contrasenia = db.Column(db.String(), unique = False, nullable = False)
    telefono = db.Column(db.String(), unique = True, nullable = False)
    dni = db.Column(db.Integer(8), unique = True, nullable = False)
    fecha_nacimiento = db.Column(db.DateTime, unique = False, nullable = False)
    fecha_creacion = db.Column(db.DateTime, default = datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default = datetime.utcnow)

    tipo = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id'), nullable = False)
    estado = db.Column(db.Integer, db.ForeignKey('estado_usuario.id'), nullable = False)

    licenia_conducir =  relationship('LicenciaConducir', backref = 'usuario')
    pasajero =  relationship('Pasajero', backref = 'usuario')
    conductor =  relationship('Conductor', backref = 'usuario')
    viaje =  relationship('Viaje', backref = 'usuario')

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
        return '<id {}>'.format(self.id)

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

class TipoUsuario(db.Model):
    __tablename__ = 'tipo_usuario'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(30), unique = True, nullable = False)
    usuarios = relationship('Usuario', backref = 'tipo_usuario')
    

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

class LicenciaConducir(db.Model):
    __tablename__ = 'licencia_conducir'
    __table_args__ = {'extend_existing': True} 


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_licencia = db.Column(db.String, unique = True, nullable = False)
    fecha_otorgamiento = db.Column(db.DateTime, unique = False, nullable = False)
    fecha_vencimiento = db.Column(db.DateTime, unique = False, nullable = False)
    imagen = db.Column(db.String(30), unique = True, nullable = False)
    
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)
    

    def __init__(self, numero_licencia, fecha_otorgamiento, fecha_vencimiento, imagen, id_usuario):
        self.numero_licencia = numero_licencia
        self.fecha_otorgamiento = fecha_otorgamiento
        self.fecha_vencimiento = fecha_vencimiento
        self.imagen = imagen
        self.id_usuario = id_usuario

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'numero_licencia': self.numero_licencia,
            'fecha_otorgamiento': self.fecha_otorgamiento,
            'fecha_vencimiento': self.fecha_vencimiento,
            'imagen': self.imagen,
            'id_usuario': self.id_usuario
    }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()