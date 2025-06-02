from flask import Blueprint, render_template
from .models import Registro

bp = Blueprint('views', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/registro')
def registro():
    return render_template('registro.html')