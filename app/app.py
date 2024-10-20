from flask import Flask, jsonify, request
import risk
from flask_cors import CORS
from sentence_transformers import SentenceTransformer


app = Flask(__name__)
CORS(app) 
model = SentenceTransformer("jxm/cde-small-v1", trust_remote_code=True)

@app.route('/get_risk', methods=['POST'])
def get_risk():
    data = request.get_json()
    description = data['description']
    return jsonify({"risk" : risk.get_risk(description, model)  })

if __name__ == '__main__':
    app.run(debug=True)