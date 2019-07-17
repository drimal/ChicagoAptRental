from flask import Flask, render_template, url_for, request
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

def predictor(list2predict):
    to_predict = np.array(list2predict).reshape(1,3)
    loaded_model = joblib.load(open("ChicagoAptRental_model.pkl","rb"))
    print(type(loaded_model))
    result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/result',methods=['POST'])
def predict():
    if request.method == 'POST':
        list2predict = request.form.to_dict()
        list2predict =list(list2predict.values())
        list2predict = list(map(int, list2predict))
        result = predictor(list2predict)
        result = "$ %d "%int(result)
        return render_template("result.html",prediction=result)

if __name__ == '__main__':
    app.run(debug=True)
