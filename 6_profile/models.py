from extensions import db
from datetime import datetime

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50), nullable=False)
    measure = db.Column(db.DateTime, nullable=False)
    temperature = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<City {self.id} {self.city_name}>"


class GeneratedImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color_hex = db.Column(db.String(7), nullable=False, unique=True)
    filename = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<GeneratedImage {self.id} {self.color_hex}>"