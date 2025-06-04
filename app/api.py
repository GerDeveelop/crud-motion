from flask import Blueprint, request, jsonify
from . import db
from .models import Registro

bp = Blueprint('api', __name__)
#ruta de crear registro
@bp.route('/registro', methods=['POST'])
def crear_registro():
    data = request.get_json()
    try:
        nuevo = Registro(
            marca=data['marca'],
            localidad=data['localidad'],
            aspirante=data['aspirante']
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"message": "Registro creado", "id": nuevo.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#ruta para obtener registros
@bp.route('/registro', methods=['GET'])
def obtener_registros():
    registros = Registro.query.all()
    return jsonify([{
        "id": r.id,
        "marca": r.marca,
        "localidad": r.localidad,
        "aspirante": r.aspirante
    } for r in registros])