LOAD DATA

INFILE 'dw_dim_payment_method.csv'
BADFILE 'dw_dim_payment_method.bad'
INTO TABLE dw_dim_payment_method
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    method_id,
    payment_method
)
