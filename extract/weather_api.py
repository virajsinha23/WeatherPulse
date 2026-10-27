
import json
from pathlib import Path

import requests

from utils.logger import get_logger

logger = get_logger(__name__)

# Find the WeatherPulse project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DATA_FILE = RAW_DATA_DIR / "weather.json"


def fetch_weather(latitude, longitude):
    """Fetch current weather data from the Open-Meteo API."""

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "pressure_msl,"
            "wind_speed_10m,"
            "rain"
        ),
    }

    try:
        logger.info(
            "Fetching weather data for latitude=%s, longitude=%s",
            latitude,
            longitude,
        )

        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        # Raise an exception if the API returns an HTTP error.
        response.raise_for_status()

        # Convert the JSON response into a Python dictionary.
        data = response.json()

        logger.info("Weather data extracted successfully.")

        return data

    except requests.RequestException:
        logger.exception("Weather API request failed.")
        raise

    except ValueError:
        logger.exception("Weather API returned invalid JSON.")
        raise


if __name__ == "__main__":
    try:
        # Example coordinates for Delhi.
        data = fetch_weather(
            latitude=28.6139,
            longitude=77.2090,
        )

        # Ensure the output directory exists.
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

        # Save the API response as a JSON file.
        with open(RAW_DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        logger.info("Raw weather data saved to %s", RAW_DATA_FILE)

        print("Weather data saved successfully.")

    except (requests.RequestException, ValueError, OSError):
        logger.exception("Weather extraction process failed.")
        print("Weather extraction failed. Check logs/weatherpulse.log.")
