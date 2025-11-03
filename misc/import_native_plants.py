#!/usr/bin/env python3
"""
Script to import native California plant data from CSV to PostgreSQL
"""

import csv
import psycopg2
from psycopg2 import sql
import re

# Database connection parameters
DB_NAME = "california_native_plants"
DB_USER = None  # Will use default user
DB_HOST = "localhost"
DB_PORT = 5432

CSV_FILE = "/Users/jacquimanzi/code/speciestrack/misc/Native To California - Sheet1.csv"

def normalize_column_name(name):
    """Convert CSV column names to database column names"""
    # Handle special case for QR Codes column
    if 'qr codes' in name.lower():
        return 'qr_codes'

    # Replace spaces and special characters with underscores
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '_', name)
    name = name.strip('_')
    return name

def clean_numeric_value(value):
    """Clean and convert numeric values"""
    if not value or value == '':
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def clean_integer_value(value):
    """Clean and convert integer values"""
    if not value or value == '':
        return None
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None

def clean_boolean_value(value):
    """Clean and convert boolean values"""
    if not value or value == '':
        return False
    value_upper = str(value).upper()
    return value_upper in ('Y', 'YES', 'TRUE', '1', 'T')

def prepare_row_data(row, headers):
    """Prepare row data with proper type conversions"""
    data = {}

    for header, value in zip(headers, row):
        db_col = normalize_column_name(header)

        # Handle empty strings
        if value == '':
            value = None

        # Special handling for specific columns
        if db_col in ['elevation_min', 'elevation_max']:
            data[db_col] = clean_integer_value(value)
        elif db_col in ['rainfall_min', 'rainfall_max', 'height_min', 'height_max', 'width_min', 'width_max']:
            data[db_col] = clean_numeric_value(value)
        elif db_col == 'is_cultivar':
            data[db_col] = clean_boolean_value(value)
        else:
            data[db_col] = value

    return data

def main():
    print(f"Starting import from {CSV_FILE}...")

    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        print(f"Connected to database '{DB_NAME}'")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return

    try:
        # Read CSV file
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)  # Get header row

            # Normalize column names
            db_columns = [normalize_column_name(h) for h in headers]

            print(f"Found {len(db_columns)} columns in CSV")
            print(f"Column mapping:")
            for orig, db in zip(headers, db_columns):
                print(f"  '{orig}' -> '{db}'")

            # Prepare INSERT statement
            insert_cols = ', '.join(db_columns)
            placeholders = ', '.join(['%s'] * len(db_columns))
            insert_query = f"""
                INSERT INTO native_plants ({insert_cols})
                VALUES ({placeholders})
                ON CONFLICT (botanical_name) DO UPDATE SET
                    {', '.join([f"{col} = EXCLUDED.{col}" for col in db_columns if col != 'botanical_name'])}
            """

            # Import rows
            row_count = 0
            error_count = 0

            for row in reader:
                try:
                    data = prepare_row_data(row, headers)
                    values = [data.get(col) for col in db_columns]

                    cur.execute(insert_query, values)
                    row_count += 1

                    if row_count % 100 == 0:
                        print(f"Imported {row_count} rows...")
                        conn.commit()

                except Exception as e:
                    error_count += 1
                    print(f"Error importing row {row_count + 1}: {e}")
                    if error_count < 5:  # Show first few errors
                        print(f"  Row data: {row[:2]}...")  # Show first columns for context
                    conn.rollback()
                    continue

            # Commit remaining rows
            conn.commit()

            print(f"\nImport complete!")
            print(f"  Successfully imported: {row_count} rows")
            print(f"  Errors: {error_count} rows")

            # Get count from database
            cur.execute("SELECT COUNT(*) FROM native_plants")
            db_count = cur.fetchone()[0]
            print(f"  Total rows in database: {db_count}")

    except Exception as e:
        print(f"Error during import: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        print("Database connection closed")

if __name__ == "__main__":
    main()
