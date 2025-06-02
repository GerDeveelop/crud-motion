from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Inicialización de extensiones
db = SQLAlchemy()

def create_app():
    # Configuración básica de Flask
    app = Flask(__name__,
                static_folder='../static',
                template_folder='../templates')
    
    # ======================
    # 1. Configuración de BD
    # ======================
    database_url = os.getenv('DATABASE_URL')
    
    # Validación crítica para producción
    if not database_url and os.getenv('RENDER') == 'true':
        raise ValueError("❌ DATABASE_URL no configurada en producción")
    
    # Fallback para desarrollo
    database_url = database_url or 'sqlite:///local.db'
    
    # Corrección para PostgreSQL en Render
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': database_url,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'pool_pre_ping': True,  # Evita conexiones muertas en Render
            'pool_recycle': 300     # Recicla conexiones cada 5 minutos
        },
        'SECRET_KEY': os.getenv('SECRET_KEY', 'dev-key-insegura')  # Para sesiones
    })
    
    # ======================
    # 2. Inicialización de DB
    # ======================
    db.init_app(app)

    
    # ======================
    # 3. Registro de Blueprints
    # ======================
    from .routes import bp as routes_blueprint  # Blueprint de rutas principales
    from .api import bp as api_blueprint       # Blueprint de API
    
    app.register_blueprint(routes_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    return app