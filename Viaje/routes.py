from flask import Blueprint, render_template
import models as modelo

viaje_bp = Blueprint('viaje_bp', __name__, url_prefix='/viaje', template_folder='templates', static_folder='static')



@viaje_bp.route('/viajes', methods=['GET', 'POST'])
def Viajes():
    viajes = modelo.Viaje.query.get(5)
    print(viajes)
    return modelo.Viaje.serialize(viajes)