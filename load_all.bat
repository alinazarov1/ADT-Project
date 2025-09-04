@echo off

sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_dim_bike_manufacturer.ctl log=dw_dim_bike_manufacturer.log
sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_dim_customer_type.ctl log=dw_dim_customer_type.log
sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_dim_payment_method.ctl log=dw_dim_payment_method.log
sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_dim_weather_condition.ctl log=dw_dim_weather_condition.log
sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_dim_membership.ctl log=dw_dim_membership.log
sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_dim_time.ctl log=dw_dim_time.log

sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_dim_country.ctl log=dw_dim_country.log
sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_dim_city.ctl log=dw_dim_city.log
sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_dim_district.ctl log=dw_dim_district.log
sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_dim_station.ctl log=dw_dim_station.log

sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_dim_bike_model.ctl log=dw_dim_bike_model.log
sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_dim_bike.ctl log=dw_dim_bike.log

sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_dim_customer.ctl log=dw_dim_customer.log
sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_dim_payment.ctl log=dw_dim_payment.log
sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_dim_weather.ctl log=dw_dim_weather.log

sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_bridge_customer_membership.ctl log=dw_bridge_customer_membership.log

sqlldr system/Alinazarov_17@alinazarov:1521/orcl control=dw_fact_bike_rental.ctl log=dw_fact_bike_rental.log
