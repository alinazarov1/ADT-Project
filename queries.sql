-- ===========================================
-- DATA WAREHOUSE ANALYTICS SQL SCRIPT
-- ===========================================

-- ===========================================
-- A. ROLLUP QUERIES
-- ===========================================

-- 1. Total revenue by country, city, district (location hierarchy)
SELECT
    co.country_name,
    ci.city_name,
    d.district_name,
    SUM(f.rental_cost) AS total_revenue
FROM dw_fact_bike_rental f
JOIN dw_dim_station s ON f.start_station_id = s.station_id
JOIN dw_dim_district d ON s.district_id = d.district_id
JOIN dw_dim_city ci ON d.city_id = ci.city_id
JOIN dw_dim_country co ON ci.country_id = co.country_id
GROUP BY ROLLUP (co.country_name, ci.city_name, d.district_name);

-- 2. Number of rentals by year, month, day
SELECT
    t.year,
    t.month_number,
    t.day_of_month,
    COUNT(*) AS total_rentals
FROM dw_fact_bike_rental f
JOIN dw_dim_time t ON f.start_time_id = t.time_id
GROUP BY ROLLUP (t.year, t.month_number, t.day_of_month);

-- 3. Revenue by bike type, manufacturer, model
SELECT
    bm.manufacturer_name,
    m.model_name,
    m.bike_type,
    SUM(f.rental_cost) AS total_revenue
FROM dw_fact_bike_rental f
JOIN dw_dim_bike b ON f.bike_id = b.bike_id
JOIN dw_dim_bike_model m ON b.model_id = m.model_id
JOIN dw_dim_bike_manufacturer bm ON m.manufacturer_id = bm.manufacturer_id
GROUP BY ROLLUP (bm.manufacturer_name, m.model_name, m.bike_type);

-- ===========================================
-- B. CUBE QUERIES
-- ===========================================

-- 1. Rentals by gender, day of week, membership type
SELECT
    c.gender,
    t.day_of_week,
    m.membership_type,
    COUNT(*) AS rental_count
FROM dw_fact_bike_rental f
JOIN dw_dim_customer c ON f.customer_id = c.customer_id
JOIN dw_dim_time t ON f.start_time_id = t.time_id
JOIN dw_bridge_customer_membership bcm ON c.customer_id = bcm.customer_id
JOIN dw_dim_membership m ON bcm.membership_id = m.membership_id
GROUP BY CUBE (c.gender, t.day_of_week, m.membership_type);

-- 2. Total revenue by station, bike type, and weather condition
SELECT
    s.station_name,
    bm.bike_type,
    wc.condition_name,
    SUM(f.rental_cost) AS total_revenue
FROM dw_fact_bike_rental f
JOIN dw_dim_station s ON f.start_station_id = s.station_id
JOIN dw_dim_bike b ON f.bike_id = b.bike_id
JOIN dw_dim_bike_model bm ON b.model_id = bm.model_id
JOIN dw_dim_weather w ON f.weather_id = w.weather_id
JOIN dw_dim_weather_condition wc ON w.condition_id = wc.condition_id
GROUP BY CUBE (s.station_name, bm.bike_type, wc.condition_name);

-- 3. Rentals by hour, city, and customer type
SELECT
    t.hour,
    ci.city_name,
    ct.customer_type,
    COUNT(*) AS rentals
FROM dw_fact_bike_rental f
JOIN dw_dim_time t ON f.start_time_id = t.time_id
JOIN dw_dim_customer c ON f.customer_id = c.customer_id
JOIN dw_dim_customer_type ct ON c.customer_type_id = ct.customer_type_id
JOIN dw_dim_station s ON f.start_station_id = s.station_id
JOIN dw_dim_district d ON s.district_id = d.district_id
JOIN dw_dim_city ci ON d.city_id = ci.city_id
GROUP BY CUBE (t.hour, ci.city_name, ct.customer_type);

-- ===========================================
-- C. PARTITION QUERIES
-- ===========================================

-- 1. Revenue share of each city within its country
SELECT
    co.country_name,
    ci.city_name,
    SUM(f.rental_cost) AS city_revenue,
    ROUND(100 * SUM(f.rental_cost) / SUM(SUM(f.rental_cost)) OVER (PARTITION BY co.country_name), 2) AS revenue_share_percent
FROM dw_fact_bike_rental f
JOIN dw_dim_station s ON f.start_station_id = s.station_id
JOIN dw_dim_district d ON s.district_id = d.district_id
JOIN dw_dim_city ci ON d.city_id = ci.city_id
JOIN dw_dim_country co ON ci.country_id = co.country_id
GROUP BY co.country_name, ci.city_name;

-- 2. Percentage of each bike type’s rentals per year
SELECT
    t.year,
    bm.bike_type,
    COUNT(*) AS rentals,
    ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY t.year), 2) AS bike_type_ratio
FROM dw_fact_bike_rental f
JOIN dw_dim_time t ON f.start_time_id = t.time_id
JOIN dw_dim_bike b ON f.bike_id = b.bike_id
JOIN dw_dim_bike_model bm ON b.model_id = bm.model_id
GROUP BY t.year, bm.bike_type;

-- 3. Payment method usage share per membership type
SELECT
    m.membership_type,
    pm.payment_method,
    COUNT(*) AS total_payments,
    ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY m.membership_type), 2) AS method_share
FROM dw_fact_bike_rental f
JOIN dw_dim_payment p ON f.payment_id = p.payment_id
JOIN dw_dim_payment_method pm ON p.method_id = pm.method_id
JOIN dw_dim_customer c ON f.customer_id = c.customer_id
JOIN dw_bridge_customer_membership bcm ON c.customer_id = bcm.customer_id
JOIN dw_dim_membership m ON bcm.membership_id = m.membership_id
GROUP BY m.membership_type, pm.payment_method;

-- ===========================================
-- D. VIEWS
-- ===========================================

-- 1. View: City-Daily Rental Stats
CREATE OR REPLACE VIEW vw_city_day_rentals AS
SELECT
    ci.city_name,
    t.day_of_month,
    t.month_number,
    t.year,
    COUNT(*) AS rental_count,
    SUM(f.rental_cost) AS total_revenue
FROM dw_fact_bike_rental f
JOIN dw_dim_time t ON f.start_time_id = t.time_id
JOIN dw_dim_station s ON f.start_station_id = s.station_id
JOIN dw_dim_district d ON s.district_id = d.district_id
JOIN dw_dim_city ci ON d.city_id = ci.city_id
GROUP BY ci.city_name, t.day_of_month, t.month_number, t.year;

-- 2. View: Manufacturer Revenue Summary
CREATE OR REPLACE VIEW vw_manufacturer_revenue AS
SELECT
    bm.manufacturer_name,
    SUM(f.rental_cost) AS total_revenue,
    COUNT(*) AS rentals
FROM dw_fact_bike_rental f
JOIN dw_dim_bike b ON f.bike_id = b.bike_id
JOIN dw_dim_bike_model m ON b.model_id = m.model_id
JOIN dw_dim_bike_manufacturer bm ON m.manufacturer_id = bm.manufacturer_id
GROUP BY bm.manufacturer_name;

-- 3. View: Daily Membership Usage by Customer Type
CREATE OR REPLACE VIEW vw_membership_daily_usage AS
SELECT
    t.year,
    t.month_number,
    t.day_of_month,
    ct.customer_type,
    m.membership_type,
    COUNT(*) AS rentals
FROM dw_fact_bike_rental f
JOIN dw_dim_time t ON f.start_time_id = t.time_id
JOIN dw_dim_customer c ON f.customer_id = c.customer_id
JOIN dw_dim_customer_type ct ON c.customer_type_id = ct.customer_type_id
JOIN dw_bridge_customer_membership bcm ON c.customer_id = bcm.customer_id
JOIN dw_dim_membership m ON bcm.membership_id = m.membership_id
GROUP BY t.year, t.month_number, t.day_of_month, ct.customer_type, m.membership_type;

-- ===========================================
-- E. RANKING FUNCTIONS
-- ===========================================

-- 1. Top 5 cities by total rental revenue
SELECT *
FROM (
    SELECT
        ci.city_name,
        co.country_name,
        SUM(f.rental_cost) AS total_revenue,
        RANK() OVER (ORDER BY SUM(f.rental_cost) DESC) AS city_rank
    FROM dw_fact_bike_rental f
    JOIN dw_dim_station s ON f.start_station_id = s.station_id
    JOIN dw_dim_district d ON s.district_id = d.district_id
    JOIN dw_dim_city ci ON d.city_id = ci.city_id
    JOIN dw_dim_country co ON ci.country_id = co.country_id
    GROUP BY ci.city_name, co.country_name
) WHERE city_rank <= 5;

-- 2. Most popular bike model per manufacturer
SELECT *
FROM (
    SELECT
        bm.manufacturer_name,
        m.model_name,
        COUNT(*) AS rentals,
        RANK() OVER (PARTITION BY bm.manufacturer_name ORDER BY COUNT(*) DESC) AS model_rank
    FROM dw_fact_bike_rental f
    JOIN dw_dim_bike b ON f.bike_id = b.bike_id
    JOIN dw_dim_bike_model m ON b.model_id = m.model_id
    JOIN dw_dim_bike_manufacturer bm ON m.manufacturer_id = bm.manufacturer_id
    GROUP BY bm.manufacturer_name, m.model_name
) WHERE model_rank = 1;

-- 3. Rank districts by number of rentals (within their city)
SELECT *
FROM (
    SELECT
        ci.city_name,
        d.district_name,
        COUNT(*) AS rental_count,
        RANK() OVER (PARTITION BY ci.city_name ORDER BY COUNT(*) DESC) AS district_rank
    FROM dw_fact_bike_rental f
    JOIN dw_dim_station s ON f.start_station_id = s.station_id
    JOIN dw_dim_district d ON s.district_id = d.district_id
    JOIN dw_dim_city ci ON d.city_id = ci.city_id
    GROUP BY ci.city_name, d.district_name
) WHERE district_rank = 1;
