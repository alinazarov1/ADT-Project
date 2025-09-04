LOAD DATA

INFILE 'dw_dim_customer_type.csv'
BADFILE 'dw_dim_customer_type.bad'
INTO TABLE dw_dim_customer_type
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    customer_type_id,
    customer_type
)
