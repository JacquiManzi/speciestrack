#!/usr/bin/env python3
"""
Script to clear all GBIF data from the database.
"""

from speciestrack.main import app
from speciestrack.models import GbifData, db

print("=" * 60)
print("Clearing GBIF Data")
print("=" * 60)

with app.app_context():
    count_before = GbifData.query.count()
    print(f"\nRecords before deletion: {count_before}")

    # Delete all records
    GbifData.query.delete()
    db.session.commit()

    count_after = GbifData.query.count()
    print(f"Records after deletion: {count_after}")

print("\n" + "=" * 60)
print("Done!")
print("=" * 60)
