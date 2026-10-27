from transform.weather_transformer import transform_weather

def test_transform_weather():
    raw_data = {
        "current": {
            "time": "2026-10-22T12:00",
            "temperature_2m": 30.5,
            "relative_humidity_2m": 65,
            "apparent_temperature": 32.0,
            "pressure_msl": 1012.0,
            "wind_speed_10m": 12.5,
            "rain": 0.0,
        }
    }
    
    df = transform_weather(raw_data, city_name = "Delhi")
    assert (len(df)) == 1
    assert df.loc[0, "city"] == "Delhi"
    assert df.loc[0, "source"] == "Open-Meteo"
    assert df.loc[0, "temperature"] == 30.5
    assert df.loc[0, "humidity"] == 65
    assert df.loc[0, "rainfall"] == 0.0
    assert "observed_at" in df.columns