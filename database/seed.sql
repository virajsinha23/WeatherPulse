iNSERT INTO cities
    (city_name, country, latitude, longitude)
VALUES
    ('Delhi', 'India', 28.6139, 77.2090),
    ('Mumbai', 'India', 19.0760, 72.8777),
    ('Bangalore', 'India', 12.9716, 77.5946),
    ('Pune', 'India', 18.5204, 73.8567),
    ('Hyderabad', 'India', 17.3850, 78.4867),
    ('Chennai', 'India', 13.0827, 80.2707),
    ('Kolkata', 'India', 22.5726, 88.3639)
ON CONFLICT (city_name)
DO NOTHING;

INSERT INTO weather_sources
(source_name, api_url)
VALUES
(
    'Open-Meteo',
    'https://api.open-meteo.com'
)
ON CONFLICT (source_name)
DO NOTHING;