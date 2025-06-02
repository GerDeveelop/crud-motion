from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configurar la base de datos con SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('postgresql://motion:bIUlznGTkHKjVpXyw4SVRzm6InfGxXUu@dpg-d0uf8n6mcj7s739kivug-a.oregon-postgres.render.com/dbmotion')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Ejemplo de modelo
class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    aspirante = db.Column(db.String(100), nullable=False)

# Crear tablas (solo para desarrollo, no usar en producción directamente)
with app.app_context():
    db.create_all()

# Ruta para crear registros (POST)
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

# Ruta para obtener registros (GET)
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
    app.run(debug=True)
