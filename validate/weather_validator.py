
import pandas as pd


def check_required_columns(df):
    required_columns = [
        "observed_at",
        "city",
        "source",
        "temperature",
        "feels_like",
        "humidity",
        "pressure",
        "wind_speed",
        "rainfall",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    return missing_columns


def check_missing_values(df):
    columns_to_check = [
        "observed_at",
        "city",
        "source",
        "temperature",
        "humidity",
    ]

    missing_values = df[columns_to_check].isnull().sum()

    return missing_values


def check_range(df):
    errors = []

    if ((df["humidity"] < 0) | (df["humidity"] > 100)).any():
        errors.append("Humidity must be between 0 and 100")

    if (df["wind_speed"] < 0).any():
        errors.append("Wind speed cannot be negative")

    if (df["rainfall"] < 0).any():
        errors.append("Rainfall cannot be negative")

    return errors


def check_duplicates(df):
    return df.duplicated().sum()


def validate_weather_data(df):
    errors = []

    # 1. Check required columns
    missing_columns = check_required_columns(df)

    if missing_columns:
        errors.append(f"Missing columns: {missing_columns}")
        return errors

    # 2. Check missing values
    missing_values = check_missing_values(df)

    if missing_values.any():
        errors.append(f"Missing values found:\n{missing_values}")

    # 3. Check value ranges
    range_errors = check_range(df)
    errors.extend(range_errors)

    # 4. Check duplicate rows
    duplicate_count = check_duplicates(df)

    if duplicate_count > 0:
        errors.append(f"Duplicate rows found: {duplicate_count}")

    return errors


if __name__ == "__main__":
    from transform.weather_transformer import (
        load_raw_weather,
        transform_weather,
    )

    data = load_raw_weather("data/raw/weather.json")

    df = transform_weather(data, city_name="Delhi")
    errors = validate_weather_data(df)

    if errors:
        print("Data validation failed")

        for error in errors:
            print("-", error)
    else:
        print("Data validation passed")

    print()
    print(df)
