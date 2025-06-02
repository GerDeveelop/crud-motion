from flask import render_template, request, jsonify
from . import db
from .models import Registro
from flask import current_app as app

@app.route('/template')
def home():
    return render_template('index.html')

@app.route('/resgistro')
def registro():
    return render_template('registro.html')

@app.route('/api/registro', methods=['POST'])
def crear_registro():
    data = request.json
    nuevo = Registro(
        marca=data['marca'],
        localidad=data['localidad'],
        aspirante=data['aspirante']
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"message": "Registro creado"}), 201

@app.route('/api/registro', methods=['GET'])
def obtener_registros():
    registros = Registro.query.all()
    return jsonify([
        {"id": r.id, "marca": r.marca, "localidad": r.localidad, "aspirante": r.aspirante}
        for r in registros
    ])
