#!/usr/bin/env python3
"""
Script to add common_name column to gbif_data table.
"""

from speciestrack.main import app, db
from sqlalchemy import text

print("=" * 60)
print("Adding common_name column to gbif_data table")
print("=" * 60)

with app.app_context():
    # Add the column using raw SQL
    sql = text("ALTER TABLE gbif_data ADD COLUMN IF NOT EXISTS common_name VARCHAR(255);")

    try:
        db.session.execute(sql)
        db.session.commit()
        print("\n✓ Successfully added common_name column to gbif_data table")
    except Exception as e:
        print(f"\n✗ Error adding column: {e}")
        db.session.rollback()

print("\n" + "=" * 60)
print("Done!")
print("=" * 60)
