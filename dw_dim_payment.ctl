LOAD DATA

INFILE 'dw_dim_payment.csv'
BADFILE 'dw_dim_payment.bad'
INTO TABLE dw_dim_payment
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    payment_id,
    method_id,
    payment_status
)
