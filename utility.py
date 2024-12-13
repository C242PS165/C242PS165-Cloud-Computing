import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder

def load_label_encoder(label_file_path):
    with open(label_file_path, 'r') as file:
        labels = file.read().splitlines()
    le = LabelEncoder()
    le.classes_ = np.array(labels)
    return le

def predict_single_data_weather(model, label_encoder, new_data_point):
    new_data_values = np.array([list(new_data_point.values())])
    prediction = model.predict(new_data_values)
    predicted_class_index = np.argmax(prediction)
    predicted_class = label_encoder.inverse_transform([predicted_class_index])[0]
    return predicted_class

def predict_single_datapoint_regression(model, datapoint, window_size=10):
    datapoint = np.array(datapoint).reshape(1, window_size, 1)
    prediction = model.predict(datapoint)
    return prediction[0][0]
