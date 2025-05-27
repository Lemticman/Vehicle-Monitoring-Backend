from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})
from config import Config

from models import db, Vehicle, Trip

app = Flask(__name__)
app.config.from_object(Config)

# Allow access only from frontend port
CORS(app, resources={r"/*": {"origins": "http://localhost:5174"}})

db.init_app(app)

@app.route("/")
def index():
    return jsonify({"message": "Vehicle Maintenance Monitoring API Running"})

@app.route("/vehicles", methods=["POST"])
def create_vehicle():
    data = request.get_json()
    new_vehicle = Vehicle(
        plate_number=data["plate_number"],
        model=data["model"],
        year=data["year"],
        mileage=data.get("mileage", 0)
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({"message": "Vehicle added successfully"}), 201

@app.route("/vehicles", methods=["GET"])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([
        {
            "id": v.id,
            "plate_number": v.plate_number,
            "model": v.model,
            "year": v.year,
            "mileage": v.mileage
        } for v in vehicles
    ])

@app.route("/vehicles/<int:id>", methods=["PUT"])
def update_vehicle(id):
    data = request.get_json()
    vehicle = Vehicle.query.get_or_404(id)
    vehicle.plate_number = data["plate_number"]
    vehicle.model = data["model"]
    vehicle.year = data["year"]
    vehicle.mileage = data["mileage"]
    db.session.commit()
    return jsonify({"message": "Vehicle updated successfully"})

@app.route("/vehicles/<int:id>", methods=["DELETE"])
def delete_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": "Vehicle deleted successfully"})

@app.route("/trips", methods=["POST"])
def create_trip():
    data = request.get_json()
    print("Received trip data:", data)
    new_trip = Trip(
        vehicle_id=data["vehicle_id"],
        date=data["date"],
        driver=data["driver"],
        start_mileage=data["start_mileage"],
        end_mileage=data["end_mileage"],
        fuel=data.get("fuel"),
        trip_details=data.get("trip_details"),
        damage=data.get("damage")
    )
    db.session.add(new_trip)
    db.session.commit()
    return jsonify({"message": "Trip logged successfully"}), 201

@app.route("/trips", methods=["GET"])
def get_trips():
    trips = Trip.query.all()
    return jsonify([
        {
            "id": t.id,
            "vehicle_id": t.vehicle_id,
            "date": t.date,
            "driver": t.driver,
            "start_mileage": t.start_mileage,
            "end_mileage": t.end_mileage,
            "fuel": t.fuel,
            "trip_details": t.trip_details,
            "damage": t.damage
        } for t in trips
    ])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
