from flask import Flask, jsonify, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

def load_model():
    model_file = open('C:\\Users\\yahaf\\OneDrive\\Desktop\\vehicles-count-pred-proj\\model\\model.pkl', 'rb')
    model = pickle.load(model_file)
    return model

def preprocess_input(datetime):
    df = pd.DataFrame({'DateTime': [datetime]})
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['Day'] = df['DateTime'].dt.day
    df['Month'] = df['DateTime'].dt.month
    df['Year'] = df['DateTime'].dt.year
    df['Hour'] = df['DateTime'].dt.hour
    # df['Minute'] = df['DateTime'].dt.minute
    df['Weekday'] = df['DateTime'].dt.weekday
    df['WeekOfYear'] = df['DateTime'].dt.isocalendar().week.astype(int)
    df['WeekOfMonth'] = (df['DateTime'].dt.day - 1) // 7 + 1
    return df.iloc[:, 1:]

@app.route('/predict', methods=['POST'])
def predict_vehicles_count():
    datetime = request.form.get('datetime')
    features = preprocess_input(datetime)
    model = load_model()

    pred = int(model.predict(features)[0])
    return jsonify({'predicted_vehicles_count': pred})

@app.route('/form', methods=['GET'])
def show_form():
    return render_template('form.html')

app.run()
