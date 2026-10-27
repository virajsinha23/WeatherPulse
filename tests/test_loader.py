from transform.weather_transformer import load_raw_weather, transform_weather
from validate.weather_validator import validate_weather_data
from load.postgres_loader import load_weather_data


def main():
    data = load_raw_weather("data/raw/weather.json")
    df = transform_weather(data, city_name="Delhi")

    errors = validate_weather_data(df)

    if errors:
        print("Data validation failed:")
        for error in errors:
            print("-", error)
        return

    print("Data validation passed.")
    load_weather_data(df)


if __name__ == "__main__":
    main()