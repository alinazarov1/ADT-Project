LOAD DATA

INFILE 'dw_dim_bike.csv'
BADFILE 'dw_dim_bike.bad'
INTO TABLE dw_dim_bike
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    bike_id,
    model_id,
    purchase_date DATE "YYYY-MM-DD",
    status
)
