from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "cce99ea13ea362d5e7a55d1bff1a654c"

@app.route("/", methods=["GET", "POST"])
def home():

    city = None
    temperature = None
    humidity = None
    description = None
    wind_speed = None
    weather_main = "clear"

    if request.method == "POST":

        city = request.form["city"]

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)

        data = response.json()

        if data["cod"] == 200:

            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]
            wind_speed = data["wind"]["speed"]
            weather_main = data["weather"][0]["main"]

    return render_template(
        "index.html",
        city=city,
        temperature=temperature,
        humidity=humidity,
        description=description,
        wind_speed=wind_speed,
        weather_main=weather_main
    )

if __name__ == "__main__":
    app.run(debug=True)