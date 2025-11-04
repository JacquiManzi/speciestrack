#!/usr/bin/env python3
"""
Script to create database tables.
Run this script to initialize your database tables.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import speciestrack
sys.path.insert(0, str(Path(__file__).parent.parent))

from speciestrack.main import app, db
from speciestrack.models import NativePlant, GbifData

print("=" * 60)
print("Creating Database Tables")
print("=" * 60)

with app.app_context():
    # Create all tables
    db.create_all()

    # Verify tables were created
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    print(f"\nTables in database: {len(tables)}")
    for table in tables:
        print(f"  - {table}")

    # Check if our expected tables exist
    expected_tables = ['native_plants', 'gbif_data']
    for table in expected_tables:
        if table in tables:
            print(f"\n✓ Table '{table}' created successfully")
        else:
            print(f"\n✗ Table '{table}' NOT found")

print("\n" + "=" * 60)
print("Database initialization complete!")
print("=" * 60)
