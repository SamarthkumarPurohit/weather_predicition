import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data = {
    "humidity": [60, 65, 70, 75, 80, 55, 50],
    "temperature": [32, 30, 28, 27, 25, 34, 36]
}

df = pd.DataFrame(data)

X = df[["humidity"]]
y = df["temperature"]

model = LinearRegression()
model.fit(X, y)

with open(os.path.join(BASE_DIR, "weather_model.pkl"), "wb") as f:
    pickle.dump(model, f)

print("Model trained successfully")
