LOAD DATA

INFILE 'dw_dim_bike_manufacturer.csv'
BADFILE 'dw_dim_bike_manufacturer.bad'
INTO TABLE dw_dim_bike_manufacturer
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    manufacturer_id,
    manufacturer_name
)
