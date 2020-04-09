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

    if comorb == 'yes':
        approp = dose_class[0]
    else:
        approp = dose_class[1]

    if comorb == 'yes':
        message = "The predicted dose to achieve a level of {} microgram/ml is {} mg. The nearest dose class is {}mg. Since, the patient has comorbidities, the recommended dose is {}mg".format(level, round(dose), dose_class, approp)
    else:
        message = "The predicted dose to achieve a level of {} microgram/ml is {} mg. The nearest dose class is {}mg. Since, the patient does not have comorbidities, the recommended dose is {}mg".format(level, round(dose), dose_class, approp)


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




