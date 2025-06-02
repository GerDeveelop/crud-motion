from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='templates')
    
    # Configuración
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///local.db').replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Registrar blueprints
    from . import routes, api
    app.register_blueprint(routes.bp)
    app.register_blueprint(api.bp, url_prefix='/api')
    
    return app