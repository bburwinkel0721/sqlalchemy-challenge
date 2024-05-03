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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation_route():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    query_results = session.query(Measurement).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()

    # Close the session
    session.close()

    # Creates a dictionary of dates and precipitation for the last year
    data_dic = {row.date:row.prcp for row in query_results}

    # Returns the jsonified data
    return jsonify(data_dic)

@app.route("/api/v1.0/stations")
def stations_route():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the station data
    query_results = session.query(Station).all()

    # Close the session
    session.close()

    # Creates a list of the station names
    data_list = [row.name for row in query_results]

    # Returns the jsonified data
    return jsonify(data_list)

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