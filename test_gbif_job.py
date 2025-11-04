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
    native_count = GbifData.query.filter_by(native=True).count()
    print(f"   Total GBIF observations in database: {total_count}")

    if total_count > 0:
        print(f"   Native plants: {native_count} ({native_count/total_count*100:.1f}%)")
        print(f"   Non-native: {total_count - native_count} ({(total_count-native_count)/total_count*100:.1f}%)")
    else:
        print("   No observations to analyze")

    # Get latest entries
    latest_entries = GbifData.query.order_by(GbifData.fetch_date.desc()).limit(10).all()

    print("\n3. Latest 10 observations:")
    for entry in latest_entries:
        native_status = "NATIVE" if entry.native else "non-native"
        print(f"   - {entry.scientific_name} [{native_status}] (count: {entry.observation_count})")

    # Show native plants
    print("\n4. Native plants observed (first 10):")
    native_plants = GbifData.query.filter_by(native=True).limit(10).all()
    if native_plants:
        for plant in native_plants:
            print(f"   - {plant.scientific_name}")
    else:
        print("   No native plants found in observations")

    # Group by fetch date
    print("\n5. Observations by fetch date:")
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
