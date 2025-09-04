
tables = [
    {
        'table_name': 'dw_dim_country',
        'infile': 'dw_dim_country.csv',
        'badfile': 'dw_dim_country.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('country_id', None),
            ('country_name', None),
        ]
    },
    {
        'table_name': 'dw_dim_bike_manufacturer',
        'infile': 'dw_dim_bike_manufacturer.csv',
        'badfile': 'dw_dim_bike_manufacturer.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('manufacturer_id', None),
            ('manufacturer_name', None),
        ]
    },
    {
        'table_name': 'dw_dim_customer_type',
        'infile': 'dw_dim_customer_type.csv',
        'badfile': 'dw_dim_customer_type.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('customer_type_id', None),
            ('customer_type', None),
        ]
    },
    {
        'table_name': 'dw_dim_payment_method',
        'infile': 'dw_dim_payment_method.csv',
        'badfile': 'dw_dim_payment_method.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('method_id', None),
            ('payment_method', None),
        ]
    },
    {
        'table_name': 'dw_dim_weather_condition',
        'infile': 'dw_dim_weather_condition.csv',
        'badfile': 'dw_dim_weather_condition.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('condition_id', None),
            ('condition_name', None),
        ]
    },
    {
        'table_name': 'dw_dim_membership',
        'infile': 'dw_dim_membership.csv',
        'badfile': 'dw_dim_membership.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('membership_id', None),
            ('membership_type', None),
            ('price', None),
            ('duration_days', None),
            ('benefits', None),
        ]
    },
    {
        'table_name': 'dw_dim_time',
        'infile': 'dw_dim_time.csv',
        'badfile': 'dw_dim_time.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('time_id', None),
            ('hour', None),
            ('day_of_week', None),
            ('day_of_month', None),
            ('month_number', None),
            ('month_name', None),
            ('quarter', None),
            ('year', None),
            ('is_weekend', None),
            ('is_holiday', None),
        ]
    },
    {
        'table_name': 'dw_dim_city',
        'infile': 'dw_dim_city.csv',
        'badfile': 'dw_dim_city.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('city_id', None),
            ('country_id', None),
            ('city_name', None),
        ]
    },
    {
        'table_name': 'dw_dim_bike_model',
        'infile': 'dw_dim_bike_model.csv',
        'badfile': 'dw_dim_bike_model.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('model_id', None),
            ('manufacturer_id', None),
            ('model_name', None),
            ('bike_type', None),
        ]
    },
    {
        'table_name': 'dw_dim_customer',
        'infile': 'dw_dim_customer.csv',
        'badfile': 'dw_dim_customer.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('customer_id', None),
            ('customer_type_id', None),
            ('registration_date', 'DATE "YYYY-MM-DD"'),
            ('birth_year', None),
            ('gender', None),
        ]
    },
    {
        'table_name': 'dw_dim_payment',
        'infile': 'dw_dim_payment.csv',
        'badfile': 'dw_dim_payment.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('payment_id', None),
            ('method_id', None),
            ('payment_status', None),
        ]
    },
    {
        'table_name': 'dw_dim_weather',
        'infile': 'dw_dim_weather.csv',
        'badfile': 'dw_dim_weather.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('weather_id', None),
            ('condition_id', None),
            ('temperature', None),
            ('precipitation', None),
            ('wind_speed', None),
            ('date_recorded', 'DATE "YYYY-MM-DD"'),
        ]
    },
    {
        'table_name': 'dw_dim_district',
        'infile': 'dw_dim_district.csv',
        'badfile': 'dw_dim_district.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('district_id', None),
            ('city_id', None),
            ('district_name', None),
            ('zip_code', None),
        ]
    },
    {
        'table_name': 'dw_dim_bike',
        'infile': 'dw_dim_bike.csv',
        'badfile': 'dw_dim_bike.bad',
        'fields_terminated_by': ',',
        'columns': [
            ('bike_id', None),
            ('model_id', None),
            ('purchase_date', 'DATE "YYYY-MM-DD"'),
            ('status', None),
        ]
    },
    {
        'table_name': 'dw_dim_station',
        'infile': 'dw_dim_station.csv',
        'badfile': 'dw_dim_station.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('station_id', None),
            ('district_id', None),
            ('station_name', None),
            ('latitude', None),
            ('longitude', None),
            ('total_capacity', None),
        ]
    },
    {
        'table_name': 'dw_bridge_customer_membership',
        'infile': 'dw_bridge_customer_membership.csv',
        'badfile': 'dw_bridge_customer_membership.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('customer_id', None),
            ('membership_id', None),
            ('start_date', 'DATE "YYYY-MM-DD"'),
            ('end_date', 'DATE "YYYY-MM-DD"'),
        ]
    },
    {
        'table_name': 'dw_fact_bike_rental',
        'infile': 'dw_fact_bike_rental.csv',
        'badfile': 'dw_fact_bike_rental.bad',
        'fields_terminated_by': ';',
        'columns': [
            ('rental_id', None),
            ('bike_id', None),
            ('start_station_id', None),
            ('end_station_id', None),
            ('start_time_id', None),
            ('end_time_id', None),
            ('customer_id', None),
            ('payment_id', None),
            ('weather_id', None),
            ('rental_duration_minutes', None),
            ('rental_cost', None),
            ('distance_km', None),
            ('calories_burned', None),
            ('carbon_saved_kg', None),
        ]
    }
]

def generate_ctl(spec):
    lines = []
    lines.append("LOAD DATA\n")
    lines.append(f"INFILE '{spec['infile']}'")
    lines.append(f"BADFILE '{spec['badfile']}'")
    lines.append(f"INTO TABLE {spec['table_name']}")
    lines.append(f"FIELDS TERMINATED BY '{spec.get('fields_terminated_by', ';')}'")
    lines.append("OPTIONALLY ENCLOSED BY '\"'")
    lines.append("TRAILING NULLCOLS")
    lines.append("(")
    
    cols = []
    for col, date_format in spec['columns']:
        if date_format:
            cols.append(f"    {col} {date_format}")
        else:
            cols.append(f"    {col}")
    
    lines.append(",\n".join(cols))
    lines.append(")\n")
    
    return "\n".join(lines)

for table in tables:
    filename = f"{table['table_name']}.ctl"
    content = generate_ctl(table)
    with open(filename, "w") as f:
        f.write(content)
    print(f"Created file: {filename}")
