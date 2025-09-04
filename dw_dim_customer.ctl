LOAD DATA

INFILE 'dw_dim_customer.csv'
BADFILE 'dw_dim_customer.bad'
INTO TABLE dw_dim_customer
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    customer_id,
    customer_type_id,
    registration_date DATE "YYYY-MM-DD",
    birth_year,
    gender
)
