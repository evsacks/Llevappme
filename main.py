from flask import Flask, jsonify, request

from routes.usuarioRoutes import usuario_api
from routes.viajeRoutes import viaje_api
from routes.vehiculoRoutes import vehiculo_api

app = Flask(__name__)

#REGISTRO LOS BLUEPRINTS
app.register_blueprint(usuario_api)
app.register_blueprint(viaje_api)
app.register_blueprint(vehiculo_api)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)