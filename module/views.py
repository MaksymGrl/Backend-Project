from module import app

@app.route("/")
def home():
    return "Hello, World"

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'OK', 200
