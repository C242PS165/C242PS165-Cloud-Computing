
# Flask Weather Prediction API

This is a simple Flask application that predicts weather based on certain input parameters such as precipitation, max temperature, min temperature, and wind speed. The app provides endpoints for both weather prediction and regression-based predictions.

## Setup Instructions

Follow the steps below to set up the environment and run the Flask app:

### 1. Create a Virtual Environment

To create a virtual environment, run the following command in your project directory:

```bash
python -m venv venv
```

This will create a `venv` directory containing the virtual environment.

### 2. Activate the Virtual Environment

- **On Windows**:
  ```bash
  venv\Scripts\activate
  ```

- **On macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

Once activated, your terminal prompt should change to indicate that you are working within the virtual environment.

### 3. Install Dependencies

With the virtual environment activated, install the dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This will install all the required Python packages for the app to run.

### 4. Run the Flask App

To start the Flask development server, run the following command:

```bash
flask run
```

This will start the server, and the application should now be running at `http://127.0.0.1:5000/`.

## API Endpoints

### `/predict/weather` [POST]

This endpoint predicts the weather based on the given data, such as precipitation, max and min temperatures, and wind speed.

#### Request Body Example:

```json
{
    "data": {
        "precipitation": 0.2,
        "temp_max": 15,
        "temp_min": 5,
        "wind": 10
    }
}
```

#### Response Example:

```json
{
    "predicted_weather": "sunny"
}
```

The response will contain the predicted weather based on the input data.

### `/predict/regression` [POST]

This endpoint predicts a regression-based value for a given model (e.g., `max_temp`) using the provided data and window size.

#### Request Body Example:

```json
{
    "model": "max_temp",
    "data": [
        1.2,
        1.5,
        1.3,
        1.8,
        1.7,
        1.4,
        1.9,
        2.0,
        1.6,
        1.8
    ],
    "window_size": 10
}
```

#### Response Example:

```json
{
  "predicted_value": 6.331772804260254
}
```

This endpoint will return the predicted value based on the regression model (e.g., `max_temp`) and the input data.

### `/predict/all` [POST]

This endpoint predicts multiple weather-related values (max temperature, min temperature, wind, precipitation) and the overall weather condition based on the provided data for all models.

#### Request Body Example:

```json
{
    "max_temp_data": [30, 32, 34, 33, 31, 30, 32, 35, 36, 37],
    "min_temp_data": [18, 19, 20, 18, 17, 16, 18, 19, 20, 21],
    "wind_data": [5, 6, 7, 6, 5, 4, 5, 6, 7, 8],
    "precipitation_data": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    "window_size": 10
}
```

#### Response Example:

```json
{
  "max_temp": 27.387659072875977,
  "min_temp": 16.518442153930664,
  "precipitation": 6.638370513916016,
  "weather": "rain",
  "wind": 6.126799583435059
}
```

This endpoint will return the predicted weather values for all models (max temperature, min temperature, wind, precipitation) and an overall weather prediction.

## Additional Notes

- Make sure to replace the actual model prediction logic and adjust the endpoints as necessary based on your actual implementation.
- This app is intended for local development use and should not be deployed as-is in production environments.

---
