
-- 6. CTE: Average temperature by city
WITH city_summary AS (
    SELECT
        c.city_name,
        AVG(w.temperature) AS avg_temperature
    FROM weather_observations w
    JOIN cities c
        ON w.city_id = c.city_id
    GROUP BY c.city_name
)
SELECT
    city_name,
    ROUND(avg_temperature::numeric, 2) AS avg_temperature
FROM city_summary
WHERE avg_temperature > 25
ORDER BY avg_temperature DESC;


-- 7. Observations above overall average
SELECT
    c.city_name,
    w.observed_at,
    w.temperature
FROM weather_observations w
JOIN cities c
    ON w.city_id = c.city_id
WHERE w.temperature > (
    SELECT AVG(temperature)
    FROM weather_observations
);


-- 8. Rank observations by temperature
SELECT
    c.city_name,
    w.observed_at,
    w.temperature,
    RANK() OVER (
        ORDER BY w.temperature DESC
    ) AS temperature_rank
FROM weather_observations w
JOIN cities c
    ON w.city_id = c.city_id;


-- 9. Compare with previous observation
SELECT
    c.city_name,
    w.observed_at,
    w.temperature,
    w.temperature - LAG(w.temperature) OVER (
        PARTITION BY c.city_id
        ORDER BY w.observed_at
    ) AS temperature_change
FROM weather_observations w
JOIN cities c
    ON w.city_id = c.city_id;


-- 10. Observations from the last 24 hours
SELECT
    c.city_name,
    w.observed_at,
    w.temperature,
    w.humidity
FROM weather_observations w
JOIN cities c
    ON w.city_id = c.city_id
WHERE w.observed_at >=
    CURRENT_TIMESTAMP - INTERVAL '24 hours'
ORDER BY w.observed_at DESC;
