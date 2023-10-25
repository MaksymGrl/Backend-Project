from module import app
from datetime import datetime
from flask import make_response
import json


@app.route("/")
def home():
    return "Backend Project Maksym G."

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    response = {
        'status': 'UP',
        'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    }
    response = json.dumps(response, indent=4)
    return make_response((response, 200, {'Content-Type': 'application/json'}))