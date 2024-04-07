from flask import Flask, request, jsonify, abort
import pickle
import numpy as np
import os

app = Flask(__name__)

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
    data = request.get_json()
    age = data['age']
    sex = data['sex']
    level = data['level']
    result = predict_dose(age, sex, level)
    return jsonify({'rounded_dose': result})

@app.route('/predict_level', methods=['POST'])
def api_predict_level():
    data = request.get_json()
    age = data['age']
    sex = data['sex']
    dose = data['dose']
    result = predict_level(age, sex, dose)
    return jsonify({'rounded_level': result})


if __name__ == '__main__':
    app.run(debug=False)
