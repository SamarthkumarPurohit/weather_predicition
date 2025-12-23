from flask import Flask, render_template, request
import requests
import pandas as pd
import pickle
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = pickle.load(open(os.path.join(BASE_DIR, "weather_model.pkl"), "rb"))

API_KEY = "8451c2e1615cf2c9b95a50921c819614"

@app.route("/", methods=["GET", "POST"])
def index():
    city = "Mumbai"
    current = None
    days = {}
    analytics = {}

    if request.method == "POST":
        city = request.form.get("city")

    # Current weather
    current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    current_data = requests.get(current_url).json()

    if current_data.get("cod") == 200:
        humidity = current_data["main"]["humidity"]
        current_temp = current_data["main"]["temp"]
        df = pd.DataFrame([[humidity]], columns=["humidity"])
        predicted = round(current_temp + (model.predict(df)[0] - current_temp) * 0.3,2)

        current = {
            "temp": current_data["main"]["temp"],
            "condition": current_data["weather"][0]["main"],
            "humidity": humidity,
            "predicted": round(predicted, 2)
        }

    # 5-day forecast
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    forecast_data = requests.get(forecast_url).json()

    if forecast_data.get("cod") == "200":
        for item in forecast_data["list"]:
            date = item["dt_txt"].split(" ")[0]
            if date not in days and len(days) < 5:
                days[date] = {
                    "temp": item["main"]["temp"],
                    "humidity": item["main"]["humidity"],
                    "wind": round(item["wind"]["speed"] * 3.6, 1),
                    "condition": item["weather"][0]["main"]
                }

        analytics = {
            "dates": list(days.keys()),
            "temps": [d["temp"] for d in days.values()],
            "humidity": [d["humidity"] for d in days.values()],
            "wind": [d["wind"] for d in days.values()]
        }

    return render_template(
        "index.html",
        city=city,
        current=current,
        days=days,
        analytics=analytics
    )

if __name__ == "__main__":
    app.run(debug=True)
