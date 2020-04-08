from flask import Flask,render_template,request
from src import predict_using_level

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/using_levels', methods=['POST'])
def using_levels():
    age = request.form.get('age')
    sex = request.form.get('sex')
    level = request.form.get('level')

    sex = 0 if sex.casefold() == "female" else 1

    dose = predict_using_level.predict_dose(age,int(sex),level)
    message = "The predicted dose to achieve a level of {} microgram/ml is {} mg".format(level,round(dose))

    return render_template('prediction.html',
                           message = message)

@app.route('/using_dose',methods=['POST'])
def using_dose():
    age = request.form.get('age')
    sex = request.form.get('sex')
    dose = request.form.get('dose')

    sex = 0 if sex.casefold() == "female" else 1

    level = predict_using_level.predict_level(age,int(sex),dose)

    message = "The predicted level using a dose of {} mg is {} microgram/ml".format(dose, level)

    return render_template('prediction.html',
                           message = message)

if __name__ == '__main__':
    app.run()




