import pandas as pd

from validate.weather_validator import validate_weather_data

def make_valid_weather_data():
    return pd.DataFrame({
        "observed_at": [pd.Timestamp("2026-10-22 12:00:00")],
        "city": ["Delhi"],
        "source": ["Open-Meteo"],
        "temperature": [30.5],
        "feels_like": [32.0],
        "humidity": [65],
        "pressure": [1012.0],
        "wind_speed": [12.5],
        "rainfall": [0.0],
    })

def test_valid_weather_data_passes():
    df = make_valid_weather_data()
    
    errors = validate_weather_data(df)
    assert errors == []
    
def test_missing_required_columns_is_detected():
    df = make_valid_weather_data().drop(columns=["temperature"])
    
    errors = validate_weather_data(df)
    
    assert any ("Missing columns" in error for error in errors)
    
def test_invalid_humidity_is_detected():
    df = make_valid_weather_data()
    df.loc[0, "humidity"] = 150
    
    errors = validate_weather_data(df)
    
    assert any ("Humidity" in error for error in errors)
    

def test_negative_wind_speed_is_detected():
    df = make_valid_weather_data()
    df.loc[0, "wind_speed"] = -5

    errors = validate_weather_data(df)

    assert any("Wind speed" in error for error in errors)

    
def test_negative_rainfall_is_detected():
    df = make_valid_weather_data()
    df.loc[0, "rainfall"] = -1

    errors = validate_weather_data(df)

    assert any("Rainfall" in error for error in errors)


def test_duplicate_rows_are_detected():
    df = make_valid_weather_data()
    df = pd.concat([df, df], ignore_index=True)

    errors = validate_weather_data(df)

    assert any("Duplicate rows" in error for error in errors)
