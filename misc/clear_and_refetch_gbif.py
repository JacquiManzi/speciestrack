#!/usr/bin/env python3
"""
Script to clear GBIF data and re-fetch with coordinates.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import speciestrack
sys.path.insert(0, str(Path(__file__).parent.parent))

from speciestrack.main import app
from speciestrack.models import GbifData, db
from speciestrack.jobs.gbif_job import store_gbif_data

print("=" * 60)
print("Clearing and Re-fetching GBIF Data")
print("=" * 60)

with app.app_context():
    # Clear existing data
    count_before = GbifData.query.count()
    print(f"\nRecords before deletion: {count_before}")

    GbifData.query.delete()
    db.session.commit()

    print(f"Records deleted: {count_before}")
    print("\n" + "=" * 60)

# Re-fetch data with coordinates
print("Fetching new data...")
print("=" * 60)
store_gbif_data(app)

print("\n" + "=" * 60)
print("Done!")
print("=" * 60)
