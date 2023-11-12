from flask import Flask, send_file, render_template
from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    return send_file('data.json', mimetype='application/json')

if __name__ == '__main__':
    app.run(host="localhost", debug=True)
