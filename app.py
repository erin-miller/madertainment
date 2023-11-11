from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    # Replace this with your actual data retrieval logic
    data = [
        {'id': 1, 'name': 'Item 1'},
        {'id': 2, 'name': 'Item 2'},
        # Add more data as needed
    ]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
