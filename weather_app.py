import requests
import geocoder
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

# ---------------- WINDOW ---------------- #

root = Tk()
root.title("Advanced Weather App")
root.geometry("700x700")
root.config(bg="#1e1e1e")

# ---------------- API KEY ---------------- #

API_KEY = "cce99ea13ea362d5e7a55d1bff1a654c"

dark_mode = True

# ---------------- FUNCTIONS ---------------- #

def toggle_mode():

    global dark_mode

    if dark_mode:
        root.config(bg="white")
        heading.config(bg="white", fg="black")
        result_label.config(bg="white", fg="black")
        city_entry.config(bg="lightgray", fg="black")
        dark_mode = False

    else:
        root.config(bg="#1e1e1e")
        heading.config(bg="#1e1e1e", fg="white")
        result_label.config(bg="#1e1e1e", fg="white")
        city_entry.config(bg="white", fg="black")
        dark_mode = True


def get_current_location():

    g = geocoder.ip('me')

    if g.city:
        city_entry.delete(0, END)
        city_entry.insert(0, g.city)

        get_weather()

    else:
        messagebox.showerror("Error", "Location not found")


def get_weather():

    city = city_entry.get()

    if city == "":
        messagebox.showerror("Error", "Please enter city name")
        return

    # ---------------- CURRENT WEATHER API ---------------- #

    current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    # ---------------- FORECAST API ---------------- #

    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    try:

        # CURRENT WEATHER
        response = requests.get(current_url)
        data = response.json()

        if response.status_code != 200:
            messagebox.showerror("Error", data["message"])
            return

        city_name = data["name"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        # ---------------- WEATHER ICON ---------------- #

        icon = data["weather"][0]["icon"]

        icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"

        icon_response = requests.get(icon_url)

        icon_image = Image.open(BytesIO(icon_response.content))
        icon_image = icon_image.resize((100, 100))

        icon_photo = ImageTk.PhotoImage(icon_image)

        weather_icon.config(image=icon_photo)
        weather_icon.image = icon_photo

        # ---------------- RESULT ---------------- #

        result_label.config(
            text=f"""
City: {city_name}

Temperature: {temp} °C

Humidity: {humidity} %

Weather: {weather}

Wind Speed: {wind_speed} m/s
"""
        )

        # ---------------- 5 DAY FORECAST ---------------- #

        forecast_response = requests.get(forecast_url)

        forecast_data = forecast_response.json()

        forecast_text = "\n\n5-Day Forecast:\n\n"

        for item in forecast_data["list"][0:5]:

            date = item["dt_txt"]
            temp = item["main"]["temp"]
            desc = item["weather"][0]["description"]

            forecast_text += f"{date}\n{temp} °C | {desc}\n\n"

        forecast_label.config(text=forecast_text)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- HEADING ---------------- #

heading = Label(
    root,
    text="Advanced Weather App",
    font=("Arial", 26, "bold"),
    bg="#1e1e1e",
    fg="white"
)

heading.pack(pady=20)

# ---------------- ENTRY ---------------- #

city_entry = Entry(
    root,
    font=("Arial", 18),
    width=25
)

city_entry.pack(pady=10)

# ---------------- BUTTONS ---------------- #

search_btn = Button(
    root,
    text="Get Weather",
    font=("Arial", 14, "bold"),
    bg="#00aaff",
    fg="white",
    command=get_weather
)

search_btn.pack(pady=10)

location_btn = Button(
    root,
    text="Current Location",
    font=("Arial", 12, "bold"),
    bg="green",
    fg="white",
    command=get_current_location
)

location_btn.pack(pady=10)

mode_btn = Button(
    root,
    text="Dark / Light Mode",
    font=("Arial", 12, "bold"),
    bg="orange",
    fg="white",
    command=toggle_mode
)

mode_btn.pack(pady=10)

# ---------------- ICON ---------------- #

weather_icon = Label(root, bg="#1e1e1e")

weather_icon.pack(pady=10)

# ---------------- RESULT ---------------- #

result_label = Label(
    root,
    text="",
    font=("Arial", 16),
    bg="#1e1e1e",
    fg="white",
    justify=LEFT
)

result_label.pack(pady=10)

# ---------------- FORECAST ---------------- #

forecast_label = Label(
    root,
    text="",
    font=("Arial", 12),
    bg="#1e1e1e",
    fg="white",
    justify=LEFT
)

forecast_label.pack(pady=20)

# ---------------- RUN ---------------- #

root.mainloop()