# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
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
        f"/api/v1.0/start=YYYY-MM-DD<start><br/>"
        f"/api/v1.0/start=YYYY-MM-DD<start>/end=YYYY-MM-DD<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation_route():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores from the last 12 months
    lastest_date = session.query(Measurement.date)\
        .order_by(Measurement.date.desc())\
        .first()
    last_year = dt.date(int(lastest_date[0][:4]),int(lastest_date[0][5:7]),int(lastest_date[0][8:]))-dt.timedelta(days=365)
    query_results = session.query(Measurement)\
        .filter(Measurement.date >= last_year)\
        .order_by(Measurement.date)\
        .all()

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
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to find the most active station by id
    most_active_station_id = session.query(Measurement.station, func.count(Measurement.station))\
    .group_by(Measurement.station)\
    .order_by(func.count(Measurement.station).desc())\
    .all()[0][0]

    # Finds the most recent date
    lastest_date = session.query(Measurement.date)\
        .filter(Measurement.station == most_active_station_id)\
        .order_by(Measurement.date.desc())\
        .first()
    
    # Calculate the date for one year ago
    last_year = dt.date(int(lastest_date[0][:4]),int(lastest_date[0][5:7]),int(lastest_date[0][8:]))-dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation values for the most active station from the last 12 months
    query_results = session.query(Measurement)\
        .filter(Measurement.date >= last_year)\
        .order_by(Measurement.date)\
        .all()

    # Close the session
    session.close()

    # Creates a dictionary of dates and precipitation for the last year
    temp_list = [row.tobs for row in query_results]

    # Returns the jsonified data
    return jsonify(temp_list)

@app.route("/api/v1.0/start=<start>")
def start_route(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation values for the most active station from the last 12 months
    query_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.sum(Measurement.tobs)/func.count(Measurement.tobs))\
    .filter(Measurement.date >= start)\
    .all()

    # Close the session
    session.close()

    # Creates a dictionary of dates and precipitation for the last year
    stats_dic = {
        'Min': query_results[0][0],
        'Max': query_results[0][1],
        'Avg': query_results[0][2]
    }

    # Returns the jsonified data
    return jsonify(stats_dic)

@app.route("/api/v1.0/start=<start>/end=<end>")
def start_end_route(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation values for the most active station from the last 12 months
    query_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.sum(Measurement.tobs)/func.count(Measurement.tobs))\
    .filter((Measurement.date >= start)&(Measurement.date <= end))\
    .all()

    # Close the session
    session.close()

    # Creates a dictionary of dates and precipitation for the last year
    data_dic = {
        'Min': query_results[0][0],
        'Max': query_results[0][1],
        'Avg': query_results[0][2]
    }

    # Returns the jsonified data
    return jsonify(data_dic)

if __name__ == '__main__':
    app.run(debug=True)