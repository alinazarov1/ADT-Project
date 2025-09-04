LOAD DATA

INFILE 'dw_dim_district.csv'
BADFILE 'dw_dim_district.bad'
INTO TABLE dw_dim_district
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    district_id,
    city_id,
    district_name,
    zip_code
)
