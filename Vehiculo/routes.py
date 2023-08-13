from flask import Blueprint, render_template

vehiculo_bp = Blueprint('vehiculo_bp', __name__, url_prefix='/vehiculo', template_folder='templates', static_folder='static')