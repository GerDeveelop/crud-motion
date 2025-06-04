from flask import Blueprint, render_template
from .models import Registro

bp = Blueprint('views', __name__)
# Ruta del template/index.html
@bp.route('/')
def home():
    return render_template('index.html')

# Ruta del template/registro.html "formulario"
@bp.route('/registro')
def registro():
    return render_template('registro.html')