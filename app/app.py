from flask import Flask, jsonify, request
import risk
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/get_risk', methods=['POST'])
def get_risk():
    data = request.get_json()
    description = data['description']
    return jsonify({"risk" : risk.get_risk(description)})

if __name__ == '__main__':
    app.run(debug=True)