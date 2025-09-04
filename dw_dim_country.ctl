LOAD DATA

INFILE 'dw_dim_country.csv'
BADFILE 'dw_dim_country.bad'
INTO TABLE dw_dim_country
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    country_id,
    country_name
)
