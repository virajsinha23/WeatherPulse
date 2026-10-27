from utils.logger import get_logger
from database.connection import get_connection

logger = get_logger(__name__)


def get_city_id(connection, city_name):
    query = """
        SELECT city_id
        FROM cities
        WHERE city_name = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (city_name,))
        result = cursor.fetchone()

    if result is None:
        raise ValueError(f"City not found: {city_name}")

    return result[0]


def get_source_id(connection, source_name):
    query = """
        SELECT source_id
        FROM weather_sources
        WHERE source_name = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (source_name,))
        result = cursor.fetchone()

    if result is None:
        raise ValueError(f"Weather source not found: {source_name}")

    return result[0]


def insert_weather_observation(connection, row, city_id, source_id):
    query = """
        INSERT INTO weather_observations (
            city_id,
            source_id,
            observed_at,
            temperature,
            feels_like,
            humidity,
            pressure,
            wind_speed,
            rainfall
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (city_id, source_id, observed_at)
        DO NOTHING
    """

    with connection.cursor() as cursor:
        cursor.execute(
            query,
            (
                city_id,
                source_id,
                row["observed_at"],
                row["temperature"],
                row["feels_like"],
                row["humidity"],
                row["pressure"],
                row["wind_speed"],
                row["rainfall"],
            ),
        )
        return cursor.rowcount == 1


def load_weather_data(df):
    if df.empty:
        logger.info("No weather observations to load.")
        return

    connection = get_connection()

    try:
        city_name = df["city"].iloc[0]
        source_name = df["source"].iloc[0]

        city_id = get_city_id(connection, city_name)
        source_id = get_source_id(connection, source_name)

        inserted_count = 0
        skipped_count = 0

        for _, row in df.iterrows():
            inserted = insert_weather_observation(
                connection,
                row,
                city_id,
                source_id,
            )

            if inserted:
                inserted_count += 1
            else:
                skipped_count += 1

        connection.commit()

        logger.info(
            "Weather load completed: %s inserted, %s skipped as duplicates.",
            inserted_count,
            skipped_count,
        )

    except Exception:
        connection.rollback()
        logger.exception("Failed to load weather observations")
        raise

    finally:
        connection.close()