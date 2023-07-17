from app import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(80), unique = False, nullable = False)
    apellido = db.Column(db.String(80), unique = False, nullable = False)
    fecha_nacimiento = db.Column(db.Date, unique = False, nullable = False)
    dni = db.Column(db.Integer(8), unique = True, nullable = False)
    email = db.Column(db.Integer, unique = True, nullable = False)
    telefono = db.Column(db.Integer, unique = True, nullable = False)
    contraseña = db.Column(db.String(80), unique = False, nullable = False)
    fecha_creacion = db.Column(db.DateTime, default = datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default = datetime.utcnow)
    estado = db.Column(db.Integer, db.ForeignKey('estado_usuario.id'))
    tipo = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id'))
    licencia_conducir = db.relationship("LicenciaConducir", back_populates="licencia")

class TipoUsuario(db.Model):
    __tablename__ = 'tipo_usuario'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(30), unique = True, nullable = False)

class EstadoUsuario(db.Model):
    __tablename__ = 'estado_usuario'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(30), unique = True, nullable = False)

class LicenciaConducir(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    licencia_nro = db.Column(db.Integer(10), unique = False, nullable = False)
    fecha_otorgamiento = db.Column(db.Date, unique = False, nullable = False)
    fecha_vencimiento = db.Column(db.Date, unique = False, nullable = False)
    imagen = db.Column(db.String(80), unique = True, nullable = False)
    observaciones = db.Column(db.String(80), unique = True, nullable = False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))