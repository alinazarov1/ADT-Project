LOAD DATA

INFILE 'dw_dim_membership.csv'
BADFILE 'dw_dim_membership.bad'
INTO TABLE dw_dim_membership
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    membership_id,
    membership_type,
    price,
    duration_days,
    benefits
)
