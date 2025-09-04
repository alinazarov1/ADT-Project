LOAD DATA

INFILE 'dw_dim_city.csv'
BADFILE 'dw_dim_city.bad'
INTO TABLE dw_dim_city
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    city_id,
    country_id,
    city_name
)
