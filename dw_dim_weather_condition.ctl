LOAD DATA

INFILE 'dw_dim_weather_condition.csv'
BADFILE 'dw_dim_weather_condition.bad'
INTO TABLE dw_dim_weather_condition
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    condition_id,
    condition_name
)
