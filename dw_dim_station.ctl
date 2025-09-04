LOAD DATA

INFILE 'dw_dim_station.csv'
BADFILE 'dw_dim_station.bad'
INTO TABLE dw_dim_station
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    station_id,
    district_id,
    station_name,
    latitude,
    longitude,
    total_capacity
)
