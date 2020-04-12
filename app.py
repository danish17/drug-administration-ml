from flask import Flask,render_template,request
from src import predict

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/using_levels', methods=['POST'])
def using_levels():
    age = request.form.get('age')
    sex = request.form.get('sex')
    level = request.form.get('level')
    comorb = request.form.get('comorb')

    sex = 0 if sex.casefold() == "female" else 1

    dose = predict.predict_dose(age,int(sex),level)
    dose_class = predict.is_close(dose)

    if (comorb == 'yes' or int(age) >= 60):
        approp = dose_class[0]
    else:
        approp = dose_class[1]

    print(dose_class)
    print(approp)

    if (comorb == 'yes' or int(age) >= 60):
        message = f'''The predicted dose to achieve a level of {level} microgram/ml is {round(dose)} mg. The dose class is {dose_class}mg. Since, the patient has comorbidities or is older than 60 years, the suggested dose is {approp}mg'''
    else:
        message = f'''The predicted dose to achieve a level of {level} microgram/ml is {round(dose)} mg. The dose class is {dose_class}mg. 
        Since, the patient does not have comorbidities, the suggested dose is {approp}mg'''

    return render_template('index.html',
                           message = message)

@app.route('/using_dose',methods=['POST'])
def using_dose():
    age = request.form.get('age')
    sex = request.form.get('sex')
    dose = request.form.get('dose')

    sex = 0 if sex.casefold() == "female" else 1

    level = predict.predict_level(age,int(sex),dose)

    message = "The predicted level using a dose of {} mg is {} microgram/ml".format(dose, level)

    return render_template('index.html',
                           message = message)

if __name__ == '__main__':
    app.run()
