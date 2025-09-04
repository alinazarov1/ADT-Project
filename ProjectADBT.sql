-- Time Dimension
CREATE TABLE dw_dim_time (
    time_id NUMBER PRIMARY KEY,
    hour NUMBER,
    day_of_week VARCHAR2(10),
    day_of_month NUMBER,
    month_number NUMBER,
    month_name VARCHAR2(10),
    quarter NUMBER,
    year NUMBER,
    is_weekend NUMBER(1),
    is_holiday NUMBER(1)
);

-- Location Hierarchy
CREATE TABLE dw_dim_country (
    country_id NUMBER PRIMARY KEY,
    country_name VARCHAR2(50)
);

CREATE TABLE dw_dim_city (
    city_id NUMBER PRIMARY KEY,
    country_id NUMBER,
    city_name VARCHAR2(50),
    CONSTRAINT fk_dw_city_country FOREIGN KEY (country_id) REFERENCES dw_dim_country(country_id)
);

CREATE TABLE dw_dim_district (
    district_id NUMBER PRIMARY KEY,
    city_id NUMBER,
    district_name VARCHAR2(50),
    zip_code VARCHAR2(10),
    CONSTRAINT fk_dw_district_city FOREIGN KEY (city_id) REFERENCES dw_dim_city(city_id)
);

-- Station Dimension
CREATE TABLE dw_dim_station (
    station_id NUMBER PRIMARY KEY,
    district_id NUMBER,
    station_name VARCHAR2(100),
    latitude NUMBER(10,6),
    longitude NUMBER(10,6),
    total_capacity NUMBER,
    CONSTRAINT fk_dw_station_district FOREIGN KEY (district_id) REFERENCES dw_dim_district(district_id)
);

-- Bike Hierarchy
CREATE TABLE dw_dim_bike_manufacturer (
    manufacturer_id NUMBER PRIMARY KEY,
    manufacturer_name VARCHAR2(50)
);

CREATE TABLE dw_dim_bike_model (
    model_id NUMBER PRIMARY KEY,
    manufacturer_id NUMBER,
    model_name VARCHAR2(50),
    bike_type VARCHAR2(50),
    CONSTRAINT fk_dw_model_manufacturer FOREIGN KEY (manufacturer_id) REFERENCES dw_dim_bike_manufacturer(manufacturer_id)
);

CREATE TABLE dw_dim_bike (
    bike_id NUMBER PRIMARY KEY,
    model_id NUMBER,
    purchase_date DATE,
    status VARCHAR2(20),
    CONSTRAINT fk_dw_bike_model FOREIGN KEY (model_id) REFERENCES dw_dim_bike_model(model_id)
);

-- Customer Hierarchy
CREATE TABLE dw_dim_customer_type (
    customer_type_id NUMBER PRIMARY KEY,
    customer_type VARCHAR2(20)
);

CREATE TABLE dw_dim_customer (
    customer_id NUMBER PRIMARY KEY,
    customer_type_id NUMBER,
    registration_date DATE,
    birth_year NUMBER(4),
    gender VARCHAR2(10),
    CONSTRAINT fk_dw_customer_type FOREIGN KEY (customer_type_id) REFERENCES dw_dim_customer_type(customer_type_id)
);

-- Membership Dimension
CREATE TABLE dw_dim_membership (
    membership_id NUMBER PRIMARY KEY,
    membership_type VARCHAR2(50),
    price NUMBER(10,2),
    duration_days NUMBER,
    benefits VARCHAR2(200)
);

-- Customer Membership Bridge
CREATE TABLE dw_bridge_customer_membership (
    customer_id NUMBER,
    membership_id NUMBER,
    start_date DATE,
    end_date DATE,
    CONSTRAINT pk_dw_bridge_cust_member PRIMARY KEY (customer_id, membership_id, start_date),
    CONSTRAINT fk_dw_bridge_customer FOREIGN KEY (customer_id) REFERENCES dw_dim_customer(customer_id),
    CONSTRAINT fk_dw_bridge_membership FOREIGN KEY (membership_id) REFERENCES dw_dim_membership(membership_id)
);

-- Payment Dimension
CREATE TABLE dw_dim_payment_method (
    method_id NUMBER PRIMARY KEY,
    payment_method VARCHAR2(50)
);

CREATE TABLE dw_dim_payment (
    payment_id NUMBER PRIMARY KEY,
    method_id NUMBER,
    payment_status VARCHAR2(20),
    CONSTRAINT fk_dw_payment_method FOREIGN KEY (method_id) REFERENCES dw_dim_payment_method(method_id)
);

-- Weather Dimension
CREATE TABLE dw_dim_weather_condition (
    condition_id NUMBER PRIMARY KEY,
    condition_name VARCHAR2(50)
);

CREATE TABLE dw_dim_weather (
    weather_id NUMBER PRIMARY KEY,
    condition_id NUMBER,
    temperature NUMBER(5,2),
    precipitation NUMBER(5,2),
    wind_speed NUMBER(5,2),
    date_recorded DATE,
    CONSTRAINT fk_dw_weather_condition FOREIGN KEY (condition_id) REFERENCES dw_dim_weather_condition(condition_id)
);

-- FACT TABLE (One fact table as requested)
CREATE TABLE dw_fact_bike_rental (
    rental_id NUMBER PRIMARY KEY,
    bike_id NUMBER,
    start_station_id NUMBER,
    end_station_id NUMBER,
    start_time_id NUMBER,
    end_time_id NUMBER,
    customer_id NUMBER,
    payment_id NUMBER,
    weather_id NUMBER,
    
    rental_duration_minutes NUMBER,
    rental_cost NUMBER(10,2),
    distance_km NUMBER(5,2),
    calories_burned NUMBER,
    carbon_saved_kg NUMBER(5,2),
    
    CONSTRAINT fk_dw_fact_bike FOREIGN KEY (bike_id) REFERENCES dw_dim_bike(bike_id),
    CONSTRAINT fk_dw_fact_start_station FOREIGN KEY (start_station_id) REFERENCES dw_dim_station(station_id),
    CONSTRAINT fk_dw_fact_end_station FOREIGN KEY (end_station_id) REFERENCES dw_dim_station(station_id),
    CONSTRAINT fk_dw_fact_start_time FOREIGN KEY (start_time_id) REFERENCES dw_dim_time(time_id),
    CONSTRAINT fk_dw_fact_end_time FOREIGN KEY (end_time_id) REFERENCES dw_dim_time(time_id),
    CONSTRAINT fk_dw_fact_customer FOREIGN KEY (customer_id) REFERENCES dw_dim_customer(customer_id),
    CONSTRAINT fk_dw_fact_payment FOREIGN KEY (payment_id) REFERENCES dw_dim_payment(payment_id),
    CONSTRAINT fk_dw_fact_weather FOREIGN KEY (weather_id) REFERENCES dw_dim_weather(weather_id)
);