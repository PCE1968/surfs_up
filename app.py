# Add dependancies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# setup database engine for the flask application to access and query our SQLite database file.
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes.
Base = automap_base()
Base.prepare(engine, reflect=True)

# create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# create a Flask application called "app."
app = Flask(__name__)

# define the welcome route
@app.route("/")

# create a function welcome()
# When creating routes, we follow the naming convention /api/v1.0/ followed by the name of the route.
# This convention signifies that this is version 1 of our application. 
# This line can be updated to support future versions of the app as well.
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# create the route for the precipitation analysis.
@app.route("/api/v1.0/precipitation")

# create the precipitation() function.
def precipitation():
    # add the line of code that calculates the date one year ago from the most recent date in the database.
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # add a query to get the date and precipitation for the previous year.
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # create a dictionary with the date as the key and the precipitation as the value.
    precip = {date: prcp for date, prcp in precipitation}
    # use jsonify() to format our results into a JSON structured file.
    return jsonify(precip)
    
