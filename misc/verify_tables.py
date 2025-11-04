#!/usr/bin/env python3
"""
Script to verify database tables and their structure.
"""

from speciestrack.main import app, db
from sqlalchemy import inspect

print("=" * 60)
print("Verifying Database Tables")
print("=" * 60)

with app.app_context():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    print(f"\nDatabase: {db.engine.url.database}")
    print(f"Total tables: {len(tables)}\n")

    for table in tables:
        print(f"\nTable: {table}")
        print("-" * 40)
        columns = inspector.get_columns(table)
        for column in columns:
            col_type = str(column['type'])
            nullable = "NULL" if column['nullable'] else "NOT NULL"
            print(f"  {column['name']:30} {col_type:20} {nullable}")

print("\n" + "=" * 60)
print("Verification complete!")
print("=" * 60)
