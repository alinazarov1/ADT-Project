LOAD DATA

INFILE 'dw_dim_bike_model.csv'
BADFILE 'dw_dim_bike_model.bad'
INTO TABLE dw_dim_bike_model
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    model_id,
    manufacturer_id,
    model_name,
    bike_type
)
