import unittest
from flask_testing import TestCase
from app import db, app
from models import Usuario, Conductor, Viaje, Ubicacion, Adicional, Pasajero, EstadoPasajero, EstadoUsuario, EstadoViaje, Vehiculo, TipoUsuario
from datetime import datetime, date, time
from flask_login import current_user

class TestBuscarViaje(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        # Agrega datos de prueba a la base de datos

        self.estado_usuario_activo = EstadoUsuario(descripcion='Activo')
        self.estado_usuario_suspendido = EstadoUsuario(descripcion='Suspendido')
        self.estado_usuario_eliminado = EstadoUsuario(descripcion='Eliminado')
        self.estado_usuario_bloqueado = EstadoUsuario(descripcion='Bloqueado')

        db.session.add(self.estado_usuario_activo)
        db.session.add(self.estado_usuario_suspendido)
        db.session.add(self.estado_usuario_eliminado)
        db.session.add(self.estado_usuario_bloqueado)

        self.tipo_usuario_pasajero = TipoUsuario(descripcion='Pasajero', codigo='P')
        self.tipo_usuario_conductor = TipoUsuario(descripcion='Conductor', codigo='C')

        db.session.add(self.tipo_usuario_conductor)
        db.session.add(self.tipo_usuario_pasajero)

        id_tipo_usuario = TipoUsuario.query.filter_by(descripcion = "Conductor").first().id
        id_estado_usuario = EstadoUsuario.query.filter_by(descripcion = "Activo").first().id

        self.user = Usuario(nombre='Evelyn', 
                            apellido='Sacks', 
                            email='evelyn@gmail.com', 
                            contrasenia='evelyn', 
                            telefono=1139553408, 
                            fecha_nacimiento=datetime.now(), 
                            fecha_creacion=datetime.now(), 
                            fecha_actualizacion=datetime.now(), 
                            id_estado_usuario=id_estado_usuario, 
                            id_tipo_usuario=id_tipo_usuario)
        db.session.add(self.user)

        self.vehiculo = Vehiculo(
            patente='NNC190',
            cantidad_asientos='5',
            fecha_creacion=datetime(2023,9,17,19,12,1,868),
            fecha_actualizacion=datetime(2023,9,17,19,12,1,868),
            descripcion='CLIO MIO BLANCO'
        )

        db.session.add(self.vehiculo)

        id_usuario = Usuario.query.first().id
        id_vehiculo = Vehiculo.query.first().id
        self.conductor = Conductor(id_usuario=id_usuario, 
                                   id_vehiculo=id_vehiculo)
        
        db.session.add(self.conductor)

        self.ubicacion = Ubicacion(
            direccion_inicial='Pilar, Buenos Aires', 
            direccion_final='Campana, Buenos Aires', 
            latitud_inicial='-34.4663154', 
            latitud_final='-34.1633346', 
            longitud_inicial='-58.9153722', 
            longitud_final='-58.95926429999999'
        )
        self.adicional = Adicional(
            mascota=True, 
            equipaje=False, 
            alimentos=False
        )
        db.session.add(self.ubicacion)
        db.session.add(self.adicional)

        self.estado_viaje_encurso = EstadoViaje(descripcion='En curso')
        self.estado_viaje_finalizado = EstadoViaje(descripcion='Finalizado')
        self.estado_viaje_pendiente = EstadoViaje(descripcion='Pendiente')
        self.estado_viaje_cancelado = EstadoViaje(descripcion='Cancelado')
        
        db.session.add(self.estado_viaje_cancelado)
        db.session.add(self.estado_viaje_encurso)
        db.session.add(self.estado_viaje_finalizado)
        db.session.add(self.estado_viaje_pendiente)
        
        id_conductor = Conductor.query.first().id
        id_ubicacion = Ubicacion.query.first().id
        id_adicional = Adicional.query.first().id
        id_estado_viaje = EstadoViaje.query.filter_by(descripcion="Pendiente").first().id
        # Crea un viaje de prueba en la base de datos
        fecha_inicio = datetime(2024,1,25,12,30)
        fecha_final = datetime(2024,1,25,13,10,50)
        
        self.viaje = Viaje(
            fecha_inicio=fecha_inicio,
            fecha_inicio_real=None,
            fecha_final_real=None,
            fecha_final=fecha_final,
            id_conductor=id_conductor,
            id_estado_viaje=id_estado_viaje,
            asientos_disponibles=3,
            id_ubicacion=id_ubicacion,
            id_adicional=id_adicional
        )
        
        db.session.add(self.viaje)
        
        self.estado_pasajero_confirmado = EstadoPasajero(descripcion='Confirmado')
        self.estado_pasajero_pendiente = EstadoPasajero(descripcion='Pendiente')
        self.estado_pasajero_rechazado = EstadoPasajero(descripcion='Rechazado')
        self.estado_pasajero_cancelado = EstadoPasajero(descripcion='Cancelado')
        self.estado_pasajero_enviaje = EstadoPasajero(descripcion='En viaje')
        self.estado_pasajero_finalizado = EstadoPasajero(descripcion='Finalizado')

        db.session.add(self.estado_pasajero_cancelado)
        db.session.add(self.estado_pasajero_confirmado)
        db.session.add(self.estado_pasajero_pendiente)
        db.session.add(self.estado_pasajero_rechazado)
        db.session.add(self.estado_pasajero_enviaje)
        db.session.add(self.estado_pasajero_finalizado)
        
        id_estado_pasajero = EstadoPasajero.query.filter_by(descripcion="Pendiente").first().id
        id_viaje = Viaje.query.first().id
        fecha_solicitud = datetime(2023,10,28,00,18,42,801)
        fecha_actualizacion = datetime(2023,10,28,1,5,50,28)
        self.pasajero = Pasajero(
            fecha_solicitud=fecha_solicitud, 
            fecha_actualizacion=fecha_actualizacion, 
            id_usuario=4, 
            id_viaje=id_viaje, 
            id_estado_pasajero=id_estado_pasajero 
        )
        
        
        db.session.add(self.pasajero)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def login(self, nombreUsuario, contrasenia):
        return self.client.post('/usuario/login', data=dict(
            nombreUsuario=nombreUsuario,
            contrasenia=contrasenia
        ), follow_redirects=True)
    
    def test_login_exitoso(self):
        # Simula un formulario de Flask para el inicio de sesión
        with self.client as client:
            response = client.post('/usuario/login', data={
                'nombreUsuario': 'evelyn@gmail.com',
                'contrasenia': 'evelyn'  # Asegúrate de que coincida con la contraseña real
            }, follow_redirects=True)

        # Verifica que la respuesta sea exitosa y el usuario esté autenticado
        self.assertEqual(response.status_code, 200)

    def test_buscar_viaje_exitoso(self):
        # Simula el proceso de inicio de sesión antes de buscar un viaje
        login_response = self.login('evelyn@gmail.com', 'evelyn')

        # Simula un formulario de Flask para buscar viaje
        with self.client as client:
            response = client.post('/viaje/buscar', data={
                'origen': 'Pilar, Buenos Aires',
                'destino': 'Campana, Buenos Aires',
                'fecha_inicio': datetime(2024,1,25,12,30)
            }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Origen', response.data)
        self.assertIn(b'Destino', response.data)

    def test_buscar_viaje_sin_resultados(self):
        # Simula el proceso de inicio de sesión antes de buscar un viaje
        login_response = self.login('evelyn@gmail.com', 'evelyn')

        # Simula un formulario de Flask para buscar viaje sin resultados
        with self.client as client:
            response = client.post('/viaje/buscar', data={
                'origen': 'OrigenNoExistente',
                'destino': 'DestinoNoExistente',
                'fecha_inicio': '2023-11-11'
            }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No se encontraron resultados', response.data)

    def test_aceptar_pasajero_exitoso(self):
        # Simula el proceso de inicio de sesión antes de buscar un viaje
        login_response = self.login('evelyn@gmail.com', 'evelyn')

        # Simula aceptar un pasajero para el viaje
        with self.client as client:
            response = client.get(f'/viaje/pasajero/{self.pasajero.id}/confirmar', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        #self.assertIn(b'Pasajero confirmado con exito', response.data)

        # Verifica que el estado del pasajero y el número de asientos disponibles se hayan actualizado
        updated_pasajero = Pasajero.query.get(self.pasajero.id)
        updated_viaje = Viaje.query.get(self.viaje.id)

        self.assertEqual(updated_pasajero.estado.descripcion, 'Confirmado')
        self.assertEqual(updated_viaje.asientos_disponibles, 2)

    def test_rechazar_pasajero_exitoso(self):
        # Simula el proceso de inicio de sesión antes de buscar un viaje
        login_response = self.login('evelyn@gmail.com', 'evelyn')

        # Simula rechazar un pasajero para el viaje
        with self.client as client:
            response = client.get(f'/viaje/pasajero/{self.pasajero.id}/rechazar', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        #self.assertIn(b'Pasajero rechazado con exito', response.data)

        # Verifica que el estado del pasajero y el número de asientos disponibles se hayan actualizado
        updated_pasajero = Pasajero.query.get(self.pasajero.id)
        updated_viaje = Viaje.query.get(self.viaje.id)

        self.assertEqual(updated_pasajero.estado.descripcion, 'Rechazado')
        self.assertEqual(updated_viaje.asientos_disponibles, 3)

    def test_publicar_viaje_exitoso(self):
        # Simula el proceso de inicio de sesión antes de buscar un viaje
        login_response = self.login('evelyn@gmail.com', 'evelyn')

        with self.client as client:
            response = client.post('/viaje/publicar', data={
                'vehiculo': 1,  # ID del vehículo existente en tu base de datos
                'origen': 'Escobar, Provincia de Buenos Aires, Argentina',
                'destino': 'Pilar, Provincia de Buenos Aires, Argentina',
                'cantidad_asientos': 3,
                'fecha_inicio': '2023-11-09',
                'hora_inicio': '12:30',
                'equipaje': True,
                'mascota': False,
                'alimentos': True
            }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        # Verifica que el viaje se haya creado en la base de datos
        ubicacion_publicado = Ubicacion.query.filter_by(
            direccion_inicial='Escobar, Provincia de Buenos Aires, Argentina',
            direccion_final='Pilar, Provincia de Buenos Aires, Argentina'
        ).first()
        viaje_publicado = Viaje.query.filter_by(id_ubicacion = ubicacion_publicado.id).first()
        self.assertIsNotNone(viaje_publicado)
        self.assertEqual(viaje_publicado.id_conductor, self.conductor.id)
        self.assertEqual(viaje_publicado.asientos_disponibles, 3)

    def test_publicar_viaje_con_errores(self):
        # Simula el proceso de inicio de sesión antes de buscar un viaje
        login_response = self.login('evelyn@gmail.com', 'evelyn')

        # Simula publicar un viaje con datos inválidos
        with self.client as client:
            response = client.post('/viaje/publicar', data={
                # Datos incompletos o incorrectos
            }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required', response.data)

    def test_unirse_viaje_exitoso(self):
        # Simula el proceso de inicio de sesión antes de unirse a un viaje
        login_response = self.login('otro_usuario@gmail.com', 'otro_usuario')

        # Simula la solicitud para unirse a un viaje
        with self.client as client:
            response = client.get(f'/viaje/solicitud/{self.viaje.id}', follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        # Verifica que el estado del pasajero se haya actualizado
        updated_pasajero = Pasajero.query.get(self.pasajero.id)
        self.assertEqual(updated_pasajero.estado.descripcion, 'Pendiente')

if __name__ == '__main__':
    unittest.main()
