
from extract.weather_api import fetch_weather
from transform.weather_transformer import transform_weather
from validate.weather_validator import validate_weather_data
from load.postgres_loader import load_weather_data
from utils.logger import get_logger

logger = get_logger(__name__)


def run_pipeline(latitude, longitude, city, country=None):
    """Run the complete WeatherPulse ETL pipeline."""

    try:
        logger.info("WeatherPulse pipeline started for %s.", city)

        # Step 1: Extract data from the weather API
        raw_data = fetch_weather(latitude, longitude)

        # Step 2: Transform the raw JSON into a DataFrame
        weather_df = transform_weather(
            raw_data,
            city_name=city,
        )

        logger.info("Weather data transformed successfully.")

        # Step 3: Validate the transformed DataFrame
        errors = validate_weather_data(weather_df)

        if errors:
            for error in errors:
                logger.error("Validation error: %s", error)

            raise ValueError(
                "Weather data validation failed. "
                "Check the log for details."
            )

        logger.info("Weather data validation passed.")

        # Step 4: Load validated data into PostgreSQL
        load_weather_data(weather_df)

        logger.info("WeatherPulse pipeline completed successfully.")

        return weather_df

    except Exception:
        logger.exception("WeatherPulse pipeline failed.")
        raise


if __name__ == "__main__":
    run_pipeline(
        latitude=28.6139,
        longitude=77.2090,
        city="Delhi",
        country="India",
    )
