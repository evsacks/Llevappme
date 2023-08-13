from flask import Blueprint, render_template

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix='/usuario', template_folder='templates', static_folder='static')