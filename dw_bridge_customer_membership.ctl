LOAD DATA

INFILE 'dw_bridge_customer_membership.csv'
BADFILE 'dw_bridge_customer_membership.bad'
INTO TABLE dw_bridge_customer_membership
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    customer_id,
    membership_id,
    start_date DATE "YYYY-MM-DD",
    end_date DATE "YYYY-MM-DD"
)
