import os
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# ================================================
# 1. Configuración Inicial de la Aplicación Flask
# ================================================
app = Flask(__name__, static_folder='../frontend/monitoring_innovation')

# ================================================
# 2. Configuración de la Base de Datos (PostgreSQL)
# ================================================
def configure_database():
    """Carga y valida la URL de la base de datos."""
    
    # Carga .env solo en desarrollo (Render usa variables de entorno directamente)
    if os.environ.get('RENDER') != 'true':
        load_dotenv()

    # Obtiene la URL de la base de datos
    database_url = os.getenv('dbmotion')
    
    # Validación crítica
    if not database_url:
        raise ValueError("❌ Error: 'DATABASE_URL' no está definida en las variables de entorno.")
    
    # Corrige el formato si es necesario (para compatibilidad con Render)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    # Configura SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Llamada a la configuración
configure_database()
db = SQLAlchemy(app)

# ================================================
# 3. Modelo de Datos (Registro)
# ================================================
class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    aspirante = db.Column(db.String(100), nullable=False)

# Crear tablas (solo en primer despliegue)
with app.app_context():
    db.create_all()

# ================================================
# 4. Rutas del Frontend (HTML/JS/CSS)
# ================================================
@app.route('/')
def serve_frontend():
    """Sirve el archivo index.html del frontend."""
    return send_from_directory(app.static_folder, 'index.html')

# ================================================
# 5. API REST (CRUD)
# ================================================
@app.route('/api/registro', methods=['POST'])
def crear_registro():
    """Crea un nuevo registro en la base de datos."""
    data = request.json
    
    try:
        nuevo_registro = Registro(
            marca=data['marca'],
            localidad=data['localidad'],
            aspirante=data['aspirante']
        )
        db.session.add(nuevo_registro)
        db.session.commit()
        return jsonify({"message": "✅ Registro creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/registro', methods=['GET'])
def obtener_registros():
    """Obtiene todos los registros de la base de datos."""
    registros = Registro.query.all()
    return jsonify([{
        "id": r.id,
        "marca": r.marca,
        "localidad": r.localidad,
        "aspirante": r.aspirante
    } for r in registros])

# ================================================
# 6. Inicio de la Aplicación
# ================================================
if __name__ == '__main__':
    # Modo desarrollo (usar 'gunicorn' en producción)
    app.run(debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true')