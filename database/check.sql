select indexname, indexdef from pg_indexes where tablename = 'weather_observations';
SELECT
    city_id,
    source_id,
    observed_at,
    COUNT(*) AS record_count
FROM weather_observations
GROUP BY city_id, source_id, observed_at
HAVING COUNT(*) > 1;

ALTER TABLE weather_observations
ADD CONSTRAINT unique_weather_observation
UNIQUE (city_id, source_id, observed_at);