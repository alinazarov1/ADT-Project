LOAD DATA

INFILE 'dw_dim_weather.csv'
BADFILE 'dw_dim_weather.bad'
INTO TABLE dw_dim_weather
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    weather_id,
    condition_id,
    temperature,
    precipitation,
    wind_speed,
    date_recorded DATE "YYYY-MM-DD"
)
