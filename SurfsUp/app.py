# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
from datetime import datetime
import dateutil.parser as parser
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

# Create our engine
engine = create_engine("sqlite+pysqlite:///SurfsUp/Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
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

# Route for our home page
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

# Route for our precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation_route():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Finds the most recent date
    lastest_date = session.query(Measurement.date)\
        .order_by(Measurement.date.desc())\
        .first()
    
    # Finds the date that is one year before the most recent date in the table
    last_year = datetime.strptime(lastest_date[0], "%Y-%m-%d").date()-dt.timedelta(days=365)

    # Perform a query to retrieve the dates and precipitation values from the last 12 months
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

# Route for our station data
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

# Route for our temperature data of the most active station
@app.route("/api/v1.0/tobs")
def tobs_route():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to find the most active station by id
    most_active_station_id = session.query(Measurement.station, func.count(Measurement.station))\
    .group_by(Measurement.station)\
    .order_by(func.count(Measurement.station).desc())\
    .all()[0][0]

    # Finds the most recent date for the most active station
    lastest_date = session.query(Measurement.date)\
        .filter(Measurement.station == most_active_station_id)\
        .order_by(Measurement.date.desc())\
        .first()
    
    # Finds the date that is one year before the most recent date of the most active station
    last_year = datetime.strptime(lastest_date[0], "%Y-%m-%d").date()-dt.timedelta(days=365)

    # Perform a query to retrieve the data for the most active station from the last 12 months
    query_results = session.query(Measurement)\
        .filter(Measurement.date >= last_year)\
        .order_by(Measurement.date)\
        .all()

    # Close the session
    session.close()

    # Creates a list of the temperatures of the most active station for the last year
    temp_list = [row.tobs for row in query_results]

    # Returns the jsonified data
    return jsonify(temp_list)

# Route for our statistics from a start date to the lastest date
@app.route("/api/v1.0/start=<start>")
def start_route(start):
    # Convert date into ISO format
    start = parser.parse(start).date()

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the min, max, and avg of all the stations from a start date to the most recent date
    query_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.sum(Measurement.tobs)/func.count(Measurement.tobs))\
    .filter(Measurement.date >= start)\
    .all()

    # Close the session
    session.close()

    # Creates a dictionary of the min, max, and avg of temperatures 
    stats_dic = {
        'Min': query_results[0][0],
        'Max': query_results[0][1],
        'Avg': query_results[0][2]
    }

    # Returns the jsonified data
    return jsonify(stats_dic)

# Route for our statistics from a start date to an end date
@app.route("/api/v1.0/start=<start>/end=<end>")
def start_end_route(start, end):
    # Converts dates into ISO format
    start = parser.parse(start).date()
    end = parser.parse(end).date()

    # Checks to see if the start date is earlier than the end date
    if start > end:
        beginning_date = end
        ending_date = start
    else:
        beginning_date = start
        ending_date = end
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the min, max, and avg of all the stations from a start date to the desired end date
    query_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.sum(Measurement.tobs)/func.count(Measurement.tobs))\
    .filter((Measurement.date >= beginning_date)&(Measurement.date <= ending_date))\
    .all()

    # Close the session
    session.close()

    # Creates a dictionary of the min, max, and avg of temperatures 
    stats_dic = {
        'Min': query_results[0][0],
        'Max': query_results[0][1],
        'Avg': query_results[0][2]
    }

    # Returns the jsonified data
    return jsonify(stats_dic)

# Runs the app
if __name__ == '__main__':
    app.run(debug=True)