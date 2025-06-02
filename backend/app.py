import os
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# ====================================
# 1. Inicialización de Flask
# ====================================
app = Flask(
    __name__,
    static_folder='../frontend/assets',           # Carpeta con los assets (JS, CSS, imágenes)
    template_folder='../frontend'                 # Carpeta base para los HTML
)

# ====================================
# 2. Configuración de la base de datos
# ====================================
def configure_database():
    if os.environ.get('RENDER') != 'true':
        load_dotenv()

    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        raise ValueError("❌ Error: 'DATABASE_URL' no está definida en las variables de entorno.")
    
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

configure_database()
db = SQLAlchemy(app)

# ====================================
# 3. Modelo de Datos
# ====================================
class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    aspirante = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

# ====================================
# 4. Rutas de HTML (Frontend)
# ====================================
@app.route('/')
def home():
    # Ruta para cargar index.html desde monitoring_innovation
    return render_template('monitoring_innovation/index.html')

@app.route('/registro')
def registro():
    # Ruta para cargar registro.html desde registro
    return render_template('registro/registro.html')

# ====================================
# 5. Rutas para archivos estáticos personalizados (JS, CSS, SVG, etc)
# ====================================
@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory(app.static_folder, filename)

# ====================================
# 6. API REST (CRUD)
# ====================================
@app.route('/api/registro', methods=['POST'])
def crear_registro():
    data = request.json
    try:
        nuevo = Registro(
            marca=data['marca'],
            localidad=data['localidad'],
            aspirante=data['aspirante']
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"message": "✅ Registro creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

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

# ====================================
# 7. Ejecución de la app
# ====================================
if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true')
