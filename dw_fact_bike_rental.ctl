LOAD DATA

INFILE 'dw_fact_bike_rental.csv'
BADFILE 'dw_fact_bike_rental.bad'
INTO TABLE dw_fact_bike_rental
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
TRAILING NULLCOLS
(
    rental_id,
    bike_id,
    start_station_id,
    end_station_id,
    start_time_id,
    end_time_id,
    customer_id,
    payment_id,
    weather_id,
    rental_duration_minutes,
    rental_cost,
    distance_km,
    calories_burned,
    carbon_saved_kg
)
