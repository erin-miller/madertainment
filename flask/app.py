from flask import Flask, jsonify, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/flask/get_data')
def get_data():
    json_file_path = os.path.join(app.root_path, 'data.json', 'data.json')
    return send_file(json_file_path, mimetype='application/json')
if __name__ == '__main__':
    app.run(port=5000, debug=True)
