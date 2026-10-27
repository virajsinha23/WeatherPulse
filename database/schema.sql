CREATE TABLE IF NOT EXISTS cities(
    city_id SERIAL PRIMARY KEY,

    city_name VARCHAR(100)
    NOT NULL
    UNIQUE,

    country VARCHAR
    NOT NULL,

    latitude DECIMAL(9,6)
    NOT NULL,

    longitude DECIMAL(9,6)
    NOT NULL
);

CREATE TABLE IF NOT EXISTS weather_sources (
    source_id SERIAL PRIMARY KEY,

    source_name VARCHAR(100)
        NOT NULL
        UNIQUE,

    api_url TEXT
        NOT NULL,

    created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS weather_observations (

    weather_id UUID
        PRIMARY KEY
        DEFAULT gen_random_uuid(),

    city_id INT
        NOT NULL,

    source_id INT
        NOT NULL,

    observed_at TIMESTAMP
        NOT NULL,

    temperature DECIMAL(5,2),

    feels_like DECIMAL(5,2),

    humidity DECIMAL(5,2),

    pressure DECIMAL(7,2),

    wind_speed DECIMAL(6,2),

    rainfall DECIMAL(7,2),

    weather_condition VARCHAR(100),

    created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_weather_city
        FOREIGN KEY (city_id)
        REFERENCES cities(city_id),

    CONSTRAINT fk_weather_source
        FOREIGN KEY (source_id)
        REFERENCES weather_sources(source_id),

    CONSTRAINT check_humidity
        CHECK (
            humidity >= 0
            AND humidity <= 100
        ),

    CONSTRAINT check_wind_speed
        CHECK (wind_speed >= 0),

    CONSTRAINT check_rainfall
        CHECK (rainfall >= 0)
);