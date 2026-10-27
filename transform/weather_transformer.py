import json
import pandas as pd

def load_raw_weather(filepath):
    with open(filepath, "r") as file:
        return json.load(file)
    
def transform_weather(data, city_name):
    current_weather = data["current"]
    
    df = pd.DataFrame([current_weather])
    
    df = df.rename(columns={
        "time" : "observed_at",
        "temperature_2m" :"temperature",
        "relative_humidity_2m" : "humidity",
        "apparent_temperature" : "feels_like",
        "pressure_msl" : "pressure",
        "wind_speed_10m" : "wind_speed",
        "rain" : "rainfall"
        
    })
    
    df["observed_at"] = pd.to_datetime(df["observed_at"])
    df["city"] = city_name
    df["source"] = "Open-Meteo"
    
    columns = [
        "observed_at",
        "city",
        "source",
        "temperature",
        "feels_like",
        "humidity",
        "pressure",
        "wind_speed",
        "rainfall"
    ]
    
    df = df[columns]
    return df

if __name__ == "__main__":
    data = load_raw_weather(
        "data/raw/weather.json"
    )
    
    df = transform_weather(
        data, city_name = "Delhi"
    )
    
    print(df)
    print()
    print(df.dtypes)