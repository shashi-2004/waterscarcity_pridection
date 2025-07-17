from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

@app.route('/')
def home():
    return render_template("Untitled-1.html")

# Load and train model
try:
    df = pd.read_excel("hyd_data (2).xlsx")
except FileNotFoundError:
    
    df = pd.DataFrame({
        'Rainfall (mm)': [800, 750, 820],
        'Population (M)': [10.7, 10.8, 10.9],
        'Demand (MGD)': [400, 410, 420],
        'Reservoir Levels (TMC)': [10, 9.5, 9.8],
        'Groundwater Usage (MGD)': [100, 105, 110],
        'Temperature (°C)': [30, 31, 29.5],
        'Available (MGD)': [300, 310, 320]
    })

df['Scarcity%'] = (df['Demand (MGD)'] - df['Available (MGD)']) / df['Demand (MGD)'] * 100

X = df[['Rainfall (mm)', 'Population (M)', 'Demand (MGD)', 
        'Reservoir Levels (TMC)', 'Groundwater Usage (MGD)', 'Temperature (°C)']]
y = df['Scarcity%']
model = RandomForestRegressor(n_estimators=100)
model.fit(X, y)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    city = data['city']
    input_data = data['input_data']
    year = int(data['year'])
    apply_adjustments = data.get('applyAdjustments', False)

    # Apply year-based adjustments
    if apply_adjustments and year > 2024:
        pop_growth = 0.025 * (year - 2024)
        input_data[1] += input_data[1] * pop_growth  # Population
        input_data[2] = input_data[1] * 20  # Demand
        input_data[4] += 5 * (year - 2024)  # Groundwater

    feature_names = ['Rainfall (mm)', 'Population (M)', 'Demand (MGD)', 
                    'Reservoir Levels (TMC)', 'Groundwater Usage (MGD)', 'Temperature (°C)']
    input_df = pd.DataFrame([input_data], columns=feature_names)

    prediction = model.predict(input_df)[0]
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)