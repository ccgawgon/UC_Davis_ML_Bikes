from flask import Flask, render_template, request, g
from season_holiday import get_season, is_holiday
from datetime import datetime
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        # Get user input from the form
        day_hour = request.form.get('day_hour')  # Datetime input
        day_hour_obj = datetime.strptime(day_hour, '%Y-%m-%dT%H:%M')
        temperature = request.form.get('temperature')  # Temperature in Celsius
        humidity = request.form.get('humidity')  # Humidity percentage
        wind_speed = request.form.get('wind_speed')  # Wind speed in m/s
        visibility = request.form.get('visibility')  # Visibility in 10m
        solar_radiation = request.form.get('solar_radiation')  # Solar radiation in Mj/m2
        rainfall = request.form.get('rainfall')  # Rainfall in mm
        snowfall = request.form.get('snowfall')  # Snowfall in cm

        # Get all season + holiday information
        season = get_season(day_hour_obj)
        has_holiday = 1 if is_holiday(day_hour_obj) else 0
        season_map = {
            "Winter": [0, 0, 0, 1],   # Jan 1 to Mar 19
            "Spring": [0, 1, 0, 0],  # Mar 20 to Jun 20
            "Summer": [0, 0, 1, 0],  # Jun 21 to Sep 21
            "Fall":   [1, 0, 0, 0],   # Sep 22 to Dec 20
        }
        season_array = season_map[season]

        # Create dataframe
        data = {
            "Hour": [day_hour_obj.hour],
            "Temperature": [temperature],
            "Humidity": [humidity],
            "Wind speed": [wind_speed],
            "Visibility": [visibility],
            "Solar Radiation": [solar_radiation],
            "Rainfall": [rainfall],
            "Snowfall": [snowfall],
            "Seasons_Autumn": [season_array[0]],
            "Seasons_Spring": [season_array[1]],
            "Seasons_Summer": [season_array[2]],
            "Seasons_Winter": [season_array[3]],
            "Holiday_No Holiday": [has_holiday]
        }
        df = pd.DataFrame(data)

        prediction = [0]

        from model import pipeline
        # Make prediction using your model
        prediction = pipeline.predict(df)  # Assuming a list input

        return render_template("result.html", prediction=prediction[0])

    else:
        return "Something went wrong. Please try again."

if __name__ == "__main__":
    app.run(debug=True)