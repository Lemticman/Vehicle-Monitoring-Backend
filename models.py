from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20), unique=True, nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    mileage = db.Column(db.Float, default=0)

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    driver = db.Column(db.String(100), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    start_mileage = db.Column(db.Integer, nullable=False)
    end_mileage = db.Column(db.Integer, nullable=False)
    fuel = db.Column(db.Float, nullable=True)
    driver = db.Column(db.String(100))
    trip_details = db.Column(db.String(255), nullable=True)
    damage = db.Column(db.String(255), nullable=True)

    vehicle = db.relationship('Vehicle', backref='trips')