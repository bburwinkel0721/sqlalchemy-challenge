# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite+pysqlite:////Users/bburwinkel/Desktop/OSU_Activities/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# # reflect the tables
Base.prepare(autoload_with=engine)

# # Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home_route():
    return "<h1>Hello, World!</h1>"

@app.route("/api/v1.0/precipitation")
def precipitation_route():
    return "<h1>Hello, World!</h1>"

@app.route("/api/v1.0/stations")
def stations_route():
    return "<h1>Hello, World!</h1>"

@app.route("/api/v1.0/tobs")
def tobs_route():
    return "<h1>Hello, World!</h1>"

@app.route("/api/v1.0/<start>")
def start_route():
    return "<h1>Hello, World!</h1>"

@app.route("/api/v1.0/<start>/<end>")
def start_end_route():
    return "<h1>Hello, World!</h1>"

if __name__ == '__main__':
    app.run(debug=True)