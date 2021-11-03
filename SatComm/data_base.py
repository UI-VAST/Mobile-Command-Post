from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import create_database as create_database_util
from sqlalchemy_utils import database_exists as database_exists_util

db = SQLAlchemy()


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.String(80), nullable=False)
    # date_time2 = db.Column(db.DateTime, nullable=False)
    external_temp = db.Column(db.Float, nullable=False)
    internal_temp = db.Column(db.Float, nullable=False)
    pressure = db.Column(db.Float, nullable=False)
    altitude = db.Column(db.Float, nullable=False)
    gps = db.Column(db.String(50), nullable=False)

    def __init__(self, date_time, external_temp, internal_temp, pressure, altitude, gps):
        self.date_time = date_time
        self.external_temp = external_temp
        self.internal_temp = internal_temp
        self.pressure = pressure
        self.altitude = altitude
        self.gps = gps


def create_database(app):
    url = make_url(app.config["SQLALCHEMY_DATABASE_URI"])
    if url.drivername == "postgres":
        url.drivername = "postgresql"

    if url.drivername.startswith("mysql"):
        url.query["charset"] = "utf8mb4"

    # Creates database if the database database does not exist
    if not database_exists_util(url):
        if url.drivername.startswith("mysql"):
            create_database_util(url, encoding="utf8mb4")
        else:
            create_database_util(url)
    return url
