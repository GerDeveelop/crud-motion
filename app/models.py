from . import db
# clase para la base de datos
class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    aspirante = db.Column(db.String(100), nullable=False)