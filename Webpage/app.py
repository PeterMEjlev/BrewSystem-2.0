from flask import Flask, jsonify, send_from_directory
import Common.variables as variables  # This is our module maintaining current brew values
from Common.variables import settings

app = Flask(__name__, static_url_path='', static_folder='static')  # serve files from /static

@app.route('/')
def index():
    # Serve the main page (index.html) which contains the frontend app
    return send_from_directory('static', 'index.html')

@app.route('/api/data')
def api_data():
    # Gather the latest values from the variables module
    status = {
        # current temperatures
        "BK_temp":    variables.temp_BK,
        "MLT_temp":   variables.temp_MLT,
        "HLT_temp":   variables.temp_HLT,

        # pot (heater) on/off
        "BK_pot":     "On" if variables.STATE["BK_ON"] else "Off",
        "HLT_pot":    "On" if variables.STATE["HLT_ON"] else "Off",

        # regulator states
        "BK_reg":     "On" if variables.BK_REG_ON else "Off",
        "HLT_reg":    "On" if variables.HLT_REG_ON else "Off",

        # pump states
        "Pump1":      "On" if variables.STATE["P1_ON"] else "Off",
        "Pump2":      "On" if variables.STATE["P2_ON"] else "Off",

        # pump efficiencies (duty cycle %)
        "Pump1_speed": f"{variables.pump_speed_P1:.0f}%",
        "Pump2_speed": f"{variables.pump_speed_P2:.0f}%", 

        # pot efficiencies
        "BK_eff":     f"{variables.settings.efficiency_BK:.0f}%",
        "HLT_eff":    f"{variables.settings.efficiency_HLT:.0f}%"
    }
    return jsonify(status)

@app.route('/api/config')
def api_config():
    """
    Returns client‐side config values, like how often to poll.
    """
    return jsonify({
        "poll_interval": settings.webpage_poll_interval
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
