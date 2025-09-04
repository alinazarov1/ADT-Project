#!/usr/bin/env python3
"""
Bike Rental Data Warehouse Generator

This script generates random data for a bike rental data warehouse, creating CSV files
for all dimension tables and the fact table with proper relationships and referential integrity.

Usage:
  python bike_rental_generator.py [options]

Options:
  -r, --rows NUMBER       Number of fact table rows to generate (default: 10000)
  -o, --output-dir DIR    Output directory for CSV files (default: current directory)
  -d, --delimiter CHAR    CSV delimiter (default: comma)
  --countries NUMBER      Number of countries to generate (default: 5)
  --cities NUMBER         Number of cities per country (default: 3)
  --districts NUMBER      Number of districts per city (default: 4)
  --stations NUMBER       Number of stations per district (default: 5)
  --manufacturers NUMBER  Number of bike manufacturers (default: 5)
  --models NUMBER         Number of models per manufacturer (default: 4)
  --bikes NUMBER          Number of bikes per model (default: 10)
  --customers NUMBER      Number of customers (default: 5000)
"""

import argparse
import csv
import random
import string
import datetime
import os
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class GeneratedData:
    """Container for all generated data to maintain relationships"""
    countries: List[Dict] = None
    cities: List[Dict] = None
    districts: List[Dict] = None
    stations: List[Dict] = None
    manufacturers: List[Dict] = None
    models: List[Dict] = None
    bikes: List[Dict] = None
    customer_types: List[Dict] = None
    customers: List[Dict] = None
    memberships: List[Dict] = None
    customer_memberships: List[Dict] = None
    payment_methods: List[Dict] = None
    payments: List[Dict] = None
    weather_conditions: List[Dict] = None
    weather: List[Dict] = None
    time_records: List[Dict] = None
    rentals: List[Dict] = None

class BikeRentalDataGenerator:
    """Data generator for bike rental data warehouse"""
    
    def __init__(self, delimiter=','):
        """Initialize the data generator"""
        self.delimiter = delimiter
        self.data = GeneratedData()
        
        # Sample data arrays
        self.country_names = ["USA", "UK", "Germany", "France", "Spain", "Italy", "Poland", "Canada", "Australia", "Japan"]
        self.city_names = ["New York", "Los Angeles", "Chicago", "London", "Paris", "Berlin", "Madrid", "Rome", 
                          "Warsaw", "Krakow", "Toronto", "Sydney", "Tokyo", "Amsterdam", "Vienna"]
        self.district_names = ["Downtown", "Riverside", "Uptown", "Historic District", "Business Center", 
                              "University Area", "Shopping District", "Residential Zone", "Park Area", "Industrial Zone"]
        self.station_prefixes = ["Central", "North", "South", "East", "West", "Main", "Park", "University", 
                                "Mall", "Station", "Terminal", "Plaza", "Square", "Gardens"]
        self.manufacturer_names = ["Trek", "Giant", "Specialized", "Cannondale", "Scott", "Merida", "Cube", "Focus"]
        self.bike_types = ["Mountain", "Road", "Hybrid", "Electric", "Cruiser", "Folding"]
        self.bike_statuses = ["Available", "In Use", "Maintenance", "Out of Service"]
        self.customer_types = ["Regular", "Premium", "Student", "Corporate"]
        self.membership_types = ["Daily", "Weekly", "Monthly", "Annual", "Student", "Corporate"]
        self.payment_methods = ["Credit Card", "Debit Card", "Cash", "Mobile Payment", "Bank Transfer"]
        self.payment_statuses = ["Completed", "Pending", "Failed", "Refunded"]
        self.weather_conditions = ["Sunny", "Cloudy", "Rainy", "Snowy", "Foggy", "Windy", "Stormy"]
        self.days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.months = ["January", "February", "March", "April", "May", "June", 
                      "July", "August", "September", "October", "November", "December"]
        
    def generate_time_dimension(self, start_year=2022, end_year=2024):
        """Generate time dimension data"""
        time_records = []
        time_id = 1
        
        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                # Generate roughly 30 time records per month (covering different hours/days)
                for day in range(1, 31, 1):  # Every day
                    try:
                        date_obj = datetime.date(year, month, day)
                        for hour in [0, 6, 12, 18]:  # 4 time periods per day
                            is_weekend = 1 if date_obj.weekday() >= 5 else 0
                            is_holiday = 1 if random.random() < 0.05 else 0  # 5% chance of holiday
                            
                            time_records.append({
                                'time_id': time_id,
                                'hour': hour,
                                'day_of_week': self.days_of_week[date_obj.weekday()],
                                'day_of_month': day,
                                'month_number': month,
                                'month_name': self.months[month-1],
                                'quarter': (month - 1) // 3 + 1,
                                'year': year,
                                'is_weekend': is_weekend,
                                'is_holiday': is_holiday
                            })
                            time_id += 1
                    except ValueError:
                        continue  # Skip invalid dates like Feb 30
                        
        self.data.time_records = time_records
        return time_records
    
    def generate_location_hierarchy(self, num_countries=5, cities_per_country=3, districts_per_city=4):
        """Generate location hierarchy: countries -> cities -> districts"""
        countries = []
        cities = []
        districts = []
        
        # Generate countries
        selected_countries = random.sample(self.country_names, min(num_countries, len(self.country_names)))
        for i, country_name in enumerate(selected_countries, 1):
            countries.append({
                'country_id': i,
                'country_name': country_name
            })
        
        # Generate cities
        city_id = 1
        selected_cities = random.sample(self.city_names, min(num_countries * cities_per_country, len(self.city_names)))
        city_idx = 0
        for country in countries:
            for _ in range(cities_per_country):
                if city_idx < len(selected_cities):
                    cities.append({
                        'city_id': city_id,
                        'country_id': country['country_id'],
                        'city_name': selected_cities[city_idx]
                    })
                    city_id += 1
                    city_idx += 1
        
        # Generate districts
        district_id = 1
        for city in cities:
            for i in range(districts_per_city):
                district_name = f"{random.choice(self.district_names)} {i+1}"
                districts.append({
                    'district_id': district_id,
                    'city_id': city['city_id'],
                    'district_name': district_name,
                    'zip_code': f"{random.randint(10000, 99999)}"
                })
                district_id += 1
        
        self.data.countries = countries
        self.data.cities = cities
        self.data.districts = districts
        return countries, cities, districts
    
    def generate_stations(self, stations_per_district=5):
        """Generate bike stations"""
        stations = []
        station_id = 1
        
        for district in self.data.districts:
            for i in range(stations_per_district):
                station_name = f"{random.choice(self.station_prefixes)} Station {i+1}"
                stations.append({
                    'station_id': station_id,
                    'district_id': district['district_id'],
                    'station_name': station_name,
                    'latitude': round(random.uniform(40.0, 55.0), 6),  # Reasonable lat range
                    'longitude': round(random.uniform(-10.0, 25.0), 6),  # Reasonable long range
                    'total_capacity': random.randint(10, 50)
                })
                station_id += 1
        
        self.data.stations = stations
        return stations
    
    def generate_bike_hierarchy(self, num_manufacturers=5, models_per_manufacturer=4, bikes_per_model=10):
        """Generate bike hierarchy: manufacturers -> models -> bikes"""
        manufacturers = []
        models = []
        bikes = []
        
        # Generate manufacturers
        selected_manufacturers = random.sample(self.manufacturer_names, min(num_manufacturers, len(self.manufacturer_names)))
        for i, manufacturer_name in enumerate(selected_manufacturers, 1):
            manufacturers.append({
                'manufacturer_id': i,
                'manufacturer_name': manufacturer_name
            })
        
        # Generate models
        model_id = 1
        for manufacturer in manufacturers:
            for i in range(models_per_manufacturer):
                model_name = f"{manufacturer['manufacturer_name']} {random.choice(self.bike_types)} {i+1}"
                models.append({
                    'model_id': model_id,
                    'manufacturer_id': manufacturer['manufacturer_id'],
                    'model_name': model_name,
                    'bike_type': random.choice(self.bike_types)
                })
                model_id += 1
        
        # Generate individual bikes
        bike_id = 1
        for model in models:
            for i in range(bikes_per_model):
                purchase_date = datetime.date(
                    random.randint(2020, 2023),
                    random.randint(1, 12),
                    random.randint(1, 28)
                )
                bikes.append({
                    'bike_id': bike_id,
                    'model_id': model['model_id'],
                    'purchase_date': purchase_date.strftime('%Y-%m-%d'),
                    'status': random.choice(self.bike_statuses)
                })
                bike_id += 1
        
        self.data.manufacturers = manufacturers
        self.data.models = models
        self.data.bikes = bikes
        return manufacturers, models, bikes
    
    def generate_customer_hierarchy(self, num_customers=5000):
        """Generate customer hierarchy and memberships"""
        customer_types = []
        customers = []
        memberships = []
        customer_memberships = []
        
        # Generate customer types
        for i, customer_type in enumerate(self.customer_types, 1):
            customer_types.append({
                'customer_type_id': i,
                'customer_type': customer_type
            })
        
        # Generate customers
        for i in range(1, num_customers + 1):
            registration_date = datetime.date(
                random.randint(2020, 2023),
                random.randint(1, 12),
                random.randint(1, 28)
            )
            customers.append({
                'customer_id': i,
                'customer_type_id': random.randint(1, len(customer_types)),
                'registration_date': registration_date.strftime('%Y-%m-%d'),
                'birth_year': random.randint(1960, 2005),
                'gender': random.choice(['Male', 'Female', 'Other'])
            })
        
        # Generate membership types
        membership_data = [
            ('Daily', 5.99, 1, 'Single day access'),
            ('Weekly', 19.99, 7, 'One week unlimited rides'),
            ('Monthly', 49.99, 30, 'One month unlimited rides'),
            ('Annual', 399.99, 365, 'Full year unlimited rides'),
            ('Student', 29.99, 30, 'Student discount monthly plan'),
            ('Corporate', 299.99, 365, 'Corporate group plan')
        ]
        
        for i, (membership_type, price, duration, benefits) in enumerate(membership_data, 1):
            memberships.append({
                'membership_id': i,
                'membership_type': membership_type,
                'price': price,
                'duration_days': duration,
                'benefits': benefits
            })
        
        # Generate customer-membership relationships
        bridge_id = 1
        for customer in customers:
            # Each customer might have 1-3 memberships over time
            num_memberships = random.randint(1, 3)
            for _ in range(num_memberships):
                membership = random.choice(memberships)
                start_date = datetime.date(
                    random.randint(2022, 2024),
                    random.randint(1, 12),
                    random.randint(1, 28)
                )
                end_date = start_date + datetime.timedelta(days=membership['duration_days'])
                
                customer_memberships.append({
                    'customer_id': customer['customer_id'],
                    'membership_id': membership['membership_id'],
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d')
                })
        
        self.data.customer_types = customer_types
        self.data.customers = customers
        self.data.memberships = memberships
        self.data.customer_memberships = customer_memberships
        return customer_types, customers, memberships, customer_memberships
    
    def generate_payment_dimension(self):
        """Generate payment dimension data"""
        payment_methods = []
        payments = []
        
        # Generate payment methods
        for i, method in enumerate(self.payment_methods, 1):
            payment_methods.append({
                'method_id': i,
                'payment_method': method
            })
        
        # Generate payment records (we'll create more during fact generation)
        for i in range(1, 1000):  # Initial payment records
            payments.append({
                'payment_id': i,
                'method_id': random.randint(1, len(payment_methods)),
                'payment_status': random.choice(self.payment_statuses)
            })
        
        self.data.payment_methods = payment_methods
        self.data.payments = payments
        return payment_methods, payments
    
    def generate_weather_dimension(self):
        """Generate weather dimension data"""
        weather_conditions = []
        weather_records = []
        
        # Generate weather conditions
        for i, condition in enumerate(self.weather_conditions, 1):
            weather_conditions.append({
                'condition_id': i,
                'condition_name': condition
            })
        
        # Generate weather records for each day in the time range
        weather_id = 1
        for year in range(2022, 2025):
            for month in range(1, 13):
                for day in range(1, 29):  # Use 28 days to avoid month issues
                    try:
                        date_obj = datetime.date(year, month, day)
                        weather_records.append({
                            'weather_id': weather_id,
                            'condition_id': random.randint(1, len(weather_conditions)),
                            'temperature': round(random.uniform(-10, 35), 2),  # Celsius
                            'precipitation': round(random.uniform(0, 50), 2),  # mm
                            'wind_speed': round(random.uniform(0, 30), 2),  # km/h
                            'date_recorded': date_obj.strftime('%Y-%m-%d')
                        })
                        weather_id += 1
                    except ValueError:
                        continue
        
        self.data.weather_conditions = weather_conditions
        self.data.weather = weather_records
        return weather_conditions, weather_records
    
    def generate_fact_rentals(self, num_rentals=10000):
        """Generate bike rental fact table data"""
        rentals = []
        
        # Ensure we have enough payment records
        while len(self.data.payments) < num_rentals:
            payment_id = len(self.data.payments) + 1
            self.data.payments.append({
                'payment_id': payment_id,
                'method_id': random.randint(1, len(self.data.payment_methods)),
                'payment_status': random.choice(self.payment_statuses)
            })
        
        for rental_id in range(1, num_rentals + 1):
            # Select random records from dimensions
            bike = random.choice(self.data.bikes)
            start_station = random.choice(self.data.stations)
            end_station = random.choice(self.data.stations)
            start_time = random.choice(self.data.time_records)
            end_time = random.choice(self.data.time_records)
            customer = random.choice(self.data.customers)
            payment = self.data.payments[rental_id - 1]  # Use corresponding payment
            weather = random.choice(self.data.weather)
            
            # Generate rental metrics
            duration_minutes = random.randint(5, 180)  # 5 minutes to 3 hours
            base_cost = random.uniform(2.0, 15.0)
            distance_km = round(random.uniform(0.5, 25.0), 2)
            calories_burned = int(duration_minutes * random.uniform(8, 12))  # Rough calculation
            carbon_saved = round(distance_km * 0.21, 2)  # Rough CO2 saved vs car
            
            rentals.append({
                'rental_id': rental_id,
                'bike_id': bike['bike_id'],
                'start_station_id': start_station['station_id'],
                'end_station_id': end_station['station_id'],
                'start_time_id': start_time['time_id'],
                'end_time_id': end_time['time_id'],
                'customer_id': customer['customer_id'],
                'payment_id': payment['payment_id'],
                'weather_id': weather['weather_id'],
                'rental_duration_minutes': duration_minutes,
                'rental_cost': round(base_cost, 2),
                'distance_km': distance_km,
                'calories_burned': calories_burned,
                'carbon_saved_kg': carbon_saved
            })
        
        self.data.rentals = rentals
        return rentals
    
    def generate_all_data(self, num_rentals=10000, **kwargs):
        """Generate all data for the data warehouse"""
        print("Generating time dimension...")
        self.generate_time_dimension()
        
        print("Generating location hierarchy...")
        self.generate_location_hierarchy(
            kwargs.get('countries', 5),
            kwargs.get('cities', 3),
            kwargs.get('districts', 4)
        )
        
        print("Generating stations...")
        self.generate_stations(kwargs.get('stations', 5))
        
        print("Generating bike hierarchy...")
        self.generate_bike_hierarchy(
            kwargs.get('manufacturers', 5),
            kwargs.get('models', 4),
            kwargs.get('bikes', 10)
        )
        
        print("Generating customer hierarchy...")
        self.generate_customer_hierarchy(kwargs.get('customers', 5000))
        
        print("Generating payment dimension...")
        self.generate_payment_dimension()
        
        print("Generating weather dimension...")
        self.generate_weather_dimension()
        
        print("Generating fact table...")
        self.generate_fact_rentals(num_rentals)
        
        print(f"Data generation complete! Generated {num_rentals} rental records.")
    
    def save_to_csv(self, output_dir='.'):
        """Save all generated data to CSV files"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Define all tables and their data
        tables = {
            'dw_dim_time.csv': self.data.time_records,
            'dw_dim_country.csv': self.data.countries,
            'dw_dim_city.csv': self.data.cities,
            'dw_dim_district.csv': self.data.districts,
            'dw_dim_station.csv': self.data.stations,
            'dw_dim_bike_manufacturer.csv': self.data.manufacturers,
            'dw_dim_bike_model.csv': self.data.models,
            'dw_dim_bike.csv': self.data.bikes,
            'dw_dim_customer_type.csv': self.data.customer_types,
            'dw_dim_customer.csv': self.data.customers,
            'dw_dim_membership.csv': self.data.memberships,
            'dw_bridge_customer_membership.csv': self.data.customer_memberships,
            'dw_dim_payment_method.csv': self.data.payment_methods,
            'dw_dim_payment.csv': self.data.payments,
            'dw_dim_weather_condition.csv': self.data.weather_conditions,
            'dw_dim_weather.csv': self.data.weather,
            'dw_fact_bike_rental.csv': self.data.rentals
        }
        
        for filename, data in tables.items():
            if data:
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    if data:
                        writer = csv.DictWriter(f, fieldnames=data[0].keys(), delimiter=self.delimiter)
                        writer.writeheader()
                        writer.writerows(data)
                        print(f"Saved {len(data)} records to {filepath}")

def main():
    parser = argparse.ArgumentParser(description='Generate bike rental data warehouse data')
    parser.add_argument('-r', '--rows', type=int, default=10000, help='Number of rental records to generate')
    parser.add_argument('-o', '--output-dir', default='.', help='Output directory for CSV files')
    parser.add_argument('-d', '--delimiter', default=',', help='CSV delimiter')
    parser.add_argument('--countries', type=int, default=5, help='Number of countries')
    parser.add_argument('--cities', type=int, default=3, help='Cities per country')
    parser.add_argument('--districts', type=int, default=4, help='Districts per city')
    parser.add_argument('--stations', type=int, default=5, help='Stations per district')
    parser.add_argument('--manufacturers', type=int, default=5, help='Number of bike manufacturers')
    parser.add_argument('--models', type=int, default=4, help='Models per manufacturer')
    parser.add_argument('--bikes', type=int, default=10, help='Bikes per model')
    parser.add_argument('--customers', type=int, default=5000, help='Number of customers')
    
    args = parser.parse_args()
    
    generator = BikeRentalDataGenerator(delimiter=args.delimiter)
    
    # Generate all data
    generator.generate_all_data(
        num_rentals=args.rows,
        countries=args.countries,
        cities=args.cities,
        districts=args.districts,
        stations=args.stations,
        manufacturers=args.manufacturers,
        models=args.models,
        bikes=args.bikes,
        customers=args.customers
    )
    
    # Save to CSV files
    generator.save_to_csv(args.output_dir)
    
    print(f"\nAll CSV files have been generated in the '{args.output_dir}' directory!")
    print(f"Generated {args.rows} bike rental records with full dimensional data.")

if __name__ == "__main__":
    main()