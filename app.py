from flask import Flask, request, jsonify, abort
import pickle
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')

def check_api_key(request):
    """Check for a valid API key in the request headers."""
    api_key = request.headers.get('X-API-KEY')
    return api_key == API_KEY

def predict_dose(age, sex, level):
    try:
        model = pickle.load(open("models/rf_dose.sav", 'rb'))
        vars = np.array([age, sex, level]).reshape(1, -1)
        calc = model.predict(vars)
        return round(calc[0])
    except Exception as e:
        return str(e)

def predict_level(age, sex, dose):
    try:
        model = pickle.load(open("models/rf_level.sav", 'rb'))
        vars = np.array([age, sex, dose]).reshape(1, -1)
        calc = model.predict(vars)
        return round(calc[0])
    except Exception as e:
        return str(e)

@app.route('/predict_dose', methods=['POST'])
def api_predict_dose():
    if not check_api_key(request):
        abort(401)  # Unauthorized access
    data = request.get_json()
    age = data['age']
    sex = data['sex']
    level = data['level']
    result = predict_dose(age, sex, level)
    return jsonify({'rounded_dose': result})

@app.route('/predict_level', methods=['POST'])
def api_predict_level():
    if not check_api_key(request):
        abort(401)  # Unauthorized access
    data = request.get_json()
    age = data['age']
    sex = data['sex']
    dose = data['dose']
    result = predict_level(age, sex, dose)
    return jsonify({'rounded_level': result})

if __name__ == '__main__':
    app.run(debug=True)
