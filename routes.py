from app import app, login_manager


from Usuario.routes import usuario_bp
from Viaje.routes import viaje_bp
from Vehiculo.routes import vehiculo_bp

import models as modelo

#Blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(vehiculo_bp)
app.register_blueprint(viaje_bp)

@login_manager.user_loader
def CargarUsuario(idUsuario):
	return modelo.Usuario.query.get(idUsuario)

#Home
@app.route('/', methods=['GET', 'POST'])
def Home():
    
    return "Hola LLEVAPPME"