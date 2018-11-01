import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


def convert_to_dict(query_result, label):
    data = []
    for record in query_result:
        data.append({'date': record[0], label: record[1]})
    return data


def most_rc_date():
    rc_date = session.query(Measurement).\
        order_by(Measurement.date.desc()).limit(1)

    for date in rc_date:
        most_rc_date = date.date

    return dt.datetime.strptime(most_rc_date, "%Y-%m-%d")

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
    )

@app.route('/api/v1.0/precipitation')
def return_precipitation():
    #most_rc_date = get_most_rc_date()
    one_ago = most_rc_date - dt.timedelta(days=365)

    rc_prcp_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_ago).\
        order_by(Measurement.date).all()

    return jsonify(convert_to_dict(rc_prcp_data, label='prcp'))


@app.route('/api/v1.0/stations')
def return_station_list():
    station_list = session.query(Measurement.station).distinct()

    return jsonify([station[0] for station in station_list])


@app.route('/api/v1.0/tobs')
def return_tobs():
    #most_rc_date = get_most_rc_date()
    one_ago = most_rc_date - dt.timedelta(days=365)

    recent_tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_ago).\
        order_by(Measurement.date).all()

    return jsonify(convert_to_dict(recent_tobs_data, label='tobs'))

if __name__ == '__main__':
    app.run(debug=True)