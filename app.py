from flask import Flask, request, jsonify
from utility import load_label_encoder, predict_single_data_weather, predict_single_datapoint_regression
import numpy as np
from tensorflow import keras

app = Flask(__name__)

# Load models and labels
classification_model = keras.models.load_model('models/weather_classification_model.h5')
max_temp_model = keras.models.load_model('models/max_temp_model.h5')
min_temp_model = keras.models.load_model('models/min_temp_model.h5')
wind_model = keras.models.load_model('models/wind_model.h5')
precipitation_model = keras.models.load_model('models/precipitation_model.h5')

label_encoder = load_label_encoder('labels.txt')


@app.route('/predict/weather', methods=['POST'])
def predict_weather():
    data = request.json
    new_data_point = data.get('data')
    result = predict_single_data_weather(classification_model, label_encoder, new_data_point)
    return jsonify({'predicted_weather': result})

@app.route('/predict/regression', methods=['POST'])
def predict_regression():
    data = request.json
    model_type = data.get('model')  # "max_temp", "min_temp", "wind", "precipitation"
    datapoint = data.get('data')
    window_size = data.get('window_size', 10)

    if model_type == 'max_temp':
        model = max_temp_model
    elif model_type == 'min_temp':
        model = min_temp_model
    elif model_type == 'wind':
        model = wind_model
    elif model_type == 'precipitation':
        model = precipitation_model
    else:
        return jsonify({'error': 'Invalid model type'}), 400

    result = float(predict_single_datapoint_regression(model, datapoint, window_size))
    return jsonify({'predicted_value': result})

@app.route('/predict/all', methods=['POST'])
def predict_all():
    data = request.json
    window_size = data.get('window_size', 10)

    # Get separate datapoints for each regression model
    max_temp_datapoint = data.get('max_temp_data')
    min_temp_datapoint = data.get('min_temp_data')
    wind_datapoint = data.get('wind_data')
    precipitation_datapoint = data.get('precipitation_data')

    # Ensure all necessary data is provided
    if not all([max_temp_datapoint, min_temp_datapoint, wind_datapoint, precipitation_datapoint]):
        return jsonify({'error': 'Missing datapoint for one or more models'}), 400

    # Predict using regression models
    max_temp_prediction = predict_single_datapoint_regression(max_temp_model, max_temp_datapoint, window_size)
    min_temp_prediction = predict_single_datapoint_regression(min_temp_model, min_temp_datapoint, window_size)
    wind_prediction = predict_single_datapoint_regression(wind_model, wind_datapoint, window_size)
    precipitation_prediction = predict_single_datapoint_regression(precipitation_model, precipitation_datapoint, window_size)

    # Ensure all predictions are converted to float if they are NumPy arrays or other types
    max_temp_prediction = float(max_temp_prediction)
    min_temp_prediction = float(min_temp_prediction)
    wind_prediction = float(wind_prediction)
    precipitation_prediction = float(precipitation_prediction)

    # Create a dictionary for weather classification input
    regression_predictions_dict = {
        'max_temp': max_temp_prediction,
        'min_temp': min_temp_prediction,
        'wind': wind_prediction,
        'precipitation': precipitation_prediction
    }

    # Predict weather using the regression results
    weather_prediction = predict_weather(regression_predictions_dict)

    # Return the predictions as a JSON response
    return jsonify({
        'weather': weather_prediction,
        'max_temp': max_temp_prediction,
        'min_temp': min_temp_prediction,
        'wind': wind_prediction,
        'precipitation': precipitation_prediction
    })

def predict_weather(new_data_point):
    result = predict_single_data_weather(classification_model, label_encoder, new_data_point)
    return result

if __name__ == '__main__':
    app.run(debug=True)
