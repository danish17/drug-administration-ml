import pickle
import numpy as np


def is_close(x):
    if x%100 >= 0 and x%100 <=50:
        ret_class = [x-x%100,x-x%100+50]
    elif x%100 >=50 and x%100 <=99:
        ret_class = [x-x%100+50,x-x%100+100]

    return ret_class

def predict_dose(age,sex,level):
    try:
        model = pickle.load(open("models/rf_dose.sav", 'rb'))
    except:
        print("\nError while loading the model...\n")

    else:
        print("Model loaded successfully...\n")

    vars = np.array([age, sex, level]).reshape(1, -1)

    calc = model.predict(vars)

    print("Calculated Dose: {}".format(calc[0]))
    print("Rounded Dose: {}".format((round(calc[0]))))

    return round(calc[0])

def predict_level(age,sex,dose):
    try:
        model = pickle.load(open("models/rf_level.sav", 'rb'))
    except:
        print("\nError while loading the model...\n")

    else:
        print("Model loaded successfully...\n")

    vars = np.array([age, sex, dose]).reshape(1, -1)

    calc = model.predict(vars)

    print("Calculated Level: {}".format(calc[0]))
    print("Rounded Level: {}".format((round(calc[0]))))

    return round(calc[0])