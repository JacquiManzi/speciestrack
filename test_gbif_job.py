#!/usr/bin/env python3
"""
Test script to manually run the GBIF data fetch and store job
"""

from speciestrack.main import app
from speciestrack.jobs.gbif_job import store_gbif_data
from speciestrack.models import GbifData

print("=" * 60)
print("Testing GBIF Data Job")
print("=" * 60)

# Run the job manually
print("\n1. Running GBIF data fetch and store job...")
store_gbif_data(app)

# Verify data was stored
with app.app_context():
    print("\n2. Verifying stored data...")

    # Count total entries
    total_count = GbifData.query.count()
    print(f"   Total GBIF observations in database: {total_count}")

    # Get latest entries
    latest_entries = GbifData.query.order_by(GbifData.fetch_date.desc()).limit(10).all()

    print("\n3. Latest 10 observations:")
    for entry in latest_entries:
        print(f"   - {entry.scientific_name} (count: {entry.observation_count}, fetched: {entry.fetch_date})")

    # Group by fetch date
    print("\n4. Observations by fetch date:")
    from sqlalchemy import func
    date_counts = GbifData.query.with_entities(
        func.date(GbifData.fetch_date).label('date'),
        func.count(GbifData.id).label('count')
    ).group_by(func.date(GbifData.fetch_date)).all()

    for date, count in date_counts:
        print(f"   {date}: {count} observations")

print("\n" + "=" * 60)
print("✓ Test complete!")
print("=" * 60)
