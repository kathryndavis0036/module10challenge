# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

#################################################
# Database Setup
#################################################

# Create an engine to connect to the SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the database into new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

# Create a new Flask application
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return "Welcome to the Climate API!"

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query to get precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()
    precip_data = {date: prcp for date, prcp in results}
    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    # Query to get all station data
    results = session.query(Station.station).all()
    stations = [station[0] for station in results]
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query to get temperature observations
    most_active_station = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()[0]
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station).all()
 

