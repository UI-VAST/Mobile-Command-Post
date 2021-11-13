import os
import configparser
from flask import Flask
from distutils.util import strtobool
from SatComm.data_base import db, Data, create_database
from SatComm.Iridium import IridiumManager


class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        envvar = os.getenv(option)
        if value == "" and envvar:
            return process_string_var(envvar)
        else:
            return value


def empty_str_cast(value, default=None):
    if value == "":
        return default
    return value


def process_string_var(value):
    if value == "":
        return None

    if value.isdigit():
        return int(value)
    elif value.replace(".", "", 1).isdigit():
        return float(value)

    try:
        return bool(strtobool(value))
    except ValueError:
        return value


def process_boolean_str(value):
    if type(value) is bool:
        return value

    if value is None:
        return False

    if value == "":
        return None

    return bool(strtobool(value))


config_ini = configparser.ConfigParser(interpolation=EnvInterpolation())
config_ini.optionxform = str  # Makes the key value case-insensitive
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
config_ini.read(path)


class ServerConfig(object):
    DATABASE_URL: str = empty_str_cast(config_ini["server"]["DATABASE_URL"]) \
        or f"sqlite:///{os.path.dirname(os.path.abspath(__file__))}/satcomm.db"

    REDIS_URL: str = empty_str_cast(config_ini["server"]["REDIS_URL"])

    SQLALCHEMY_DATABASE_URI = DATABASE_URL

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = process_boolean_str(empty_str_cast(config_ini["optional"]["SQLALCHEMY_TRACK_MODIFICATIONS"], default=False))


def create_app():
    # If `entrypoint` is not defined in app.yaml, App Engine will look for an app
    # called `app` in `main.py`.
    app = Flask(__name__)
    with app.app_context():
        app.config.from_object(ServerConfig)
        app.config['SQLALCHEMY_DATABASE_URI'] = str(create_database(app))
        db.init_app(app)
        db.create_all()

        print("Starting Iridium Package.")
        IR = IridiumManager()
        print("Starting Listener.")
        IR.ir.listen()
        # print("Starting Saver.")
        # IR.SaveMessage()
        print("Iridium Package Started.")

        from SatComm.view import view
        app.register_blueprint(view)

    return app


app = create_app()
app.run()
