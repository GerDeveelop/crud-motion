from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__, static_folder='../frontend/monitoring_innovation')

# Configurar la base de datos con SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de datos
class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    aspirante = db.Column(db.String(100), nullable=False)

# Crear tablas (solo en primer despliegue)
with app.app_context():
    db.create_all()

# Servir frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

# API Routes
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
        {
            "id": r.id,
            "marca": r.marca,
            "localidad": r.localidad,
            "aspirante": r.aspirante
        } for r in registros
    ])

if __name__ == '__main__':
    app.run()