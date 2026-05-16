from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "cce99ea13ea362d5e7a55d1bff1a654c"

@app.route('/', methods=['GET', 'POST'])
def home():

    weather_data = None
    forecast_data = []

    background = "default"

    if request.method == 'POST':

        city = request.form['city']

        # CURRENT WEATHER

        current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(current_url)

        data = response.json()

        if response.status_code == 200:

            weather_type = data["weather"][0]["main"]

            # DYNAMIC BACKGROUND

            if weather_type == "Rain":

                background = "rain"

            elif weather_type == "Clouds":

                background = "clouds"

            elif weather_type == "Clear":

                background = "clear"

            else:

                background = "default"

            weather_data = {

                "city": data["name"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "weather": data["weather"][0]["description"],
                "wind": data["wind"]["speed"],
                "icon": data["weather"][0]["icon"]
            }

            # FORECAST

            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

            forecast_response = requests.get(forecast_url)

            forecast_json = forecast_response.json()

            added_days = []

            for item in forecast_json["list"]:

                date = item["dt_txt"]

                day = date.split(" ")[0]

                day_name = datetime.strptime(
                    day,
                    "%Y-%m-%d"
                ).strftime("%a")

                if day_name not in added_days:

                    added_days.append(day_name)

                    forecast_data.append({

                        "day": day_name,
                        "temp": item["main"]["temp"],
                        "icon": item["weather"][0]["icon"]
                    })

                if len(forecast_data) == 7:

                    break

        else:

            weather_data = {

                "error": "City not found"
            }

    return render_template(

        'index.html',

        weather=weather_data,

        forecast=forecast_data,

        background=background
    )

if __name__ == '__main__':

    app.run(debug=True)