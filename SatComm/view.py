from flask import Blueprint, request, abort, render_template

from SatComm.data_base import db, Data
from SatComm.hex_to_ascii import hex_to_ascii, remove_spaces

view = Blueprint("view", __name__)

# outside temp C, inside temp c, pressure pascal, altitude m, gps data


@view.route("/", methods=["GET"])
def index():
    data = Data.query.order_by(Data.id.desc()).first()
    if data is not None:
        latest_data = {"ext_temp": data.external_temp, "int_temp": data.internal_temp, "press": data.pressure, "alt": data.altitude, "gps": data.gps}
    else:
        latest_data = {"ext_temp": "NUL", "int_temp": "NUL", "press": "NUL", "alt": "NUL", "gps": "NUL"}
    return render_template("index.html", data=latest_data)


@view.route("/webhook", methods=['POST'])
def webhook():
    if request.method == 'POST':
        income = request.json
        print(income)
        hook_data = remove_spaces(hex_to_ascii(income["data"]))
        data = Data("", float(hook_data[0]), float(hook_data[1]), float(hook_data[2]), float(hook_data[3]), hook_data[4] + " " + hook_data[5])
        db.session.add(data)
        db.session.commit()
        return 'success :)', 200
    else:
        abort(400, "Data type not correct", custom=request.method)
