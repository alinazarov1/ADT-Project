LOAD DATA

INFILE 'dw_dim_time.csv'
BADFILE 'dw_dim_time.bad'
INTO TABLE dw_dim_time
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    time_id,
    hour,
    day_of_week,
    day_of_month,
    month_number,
    month_name,
    quarter,
    year,
    is_weekend,
    is_holiday
)
