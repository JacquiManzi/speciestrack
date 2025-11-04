#!/usr/bin/env python3
"""
Script to check GBIF data in the database.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import speciestrack
sys.path.insert(0, str(Path(__file__).parent.parent))

from speciestrack.main import app
from speciestrack.models import GbifData
from sqlalchemy import func

print("=" * 60)
print("Checking GBIF Data in Database")
print("=" * 60)

with app.app_context():
    # Count total entries
    total_count = GbifData.query.count()
    native_count = GbifData.query.filter_by(native=True).count()
    non_native_count = GbifData.query.filter_by(native=False).count()

    print(f"\nTotal GBIF observations: {total_count}")
    print(f"Native plants: {native_count} ({native_count/total_count*100:.1f}%)")
    print(f"Non-native: {non_native_count} ({non_native_count/total_count*100:.1f}%)")

    # Show top 10 native plants by observation count
    print("\n" + "=" * 60)
    print("Top 10 Native Plants (by observation count)")
    print("=" * 60)
    native_plants = GbifData.query.filter_by(native=True).order_by(
        GbifData.observation_count.desc()
    ).limit(10).all()

    for i, plant in enumerate(native_plants, 1):
        print(f"{i:2}. {plant.scientific_name:50} ({plant.observation_count} observations)")

    # Show top 10 non-native species
    print("\n" + "=" * 60)
    print("Top 10 Non-Native Species (by observation count)")
    print("=" * 60)
    non_native = GbifData.query.filter_by(native=False).order_by(
        GbifData.observation_count.desc()
    ).limit(10).all()

    for i, species in enumerate(non_native, 1):
        print(f"{i:2}. {species.scientific_name:50} ({species.observation_count} observations)")

    # Group by fetch date
    print("\n" + "=" * 60)
    print("Observations by Fetch Date")
    print("=" * 60)
    date_counts = GbifData.query.with_entities(
        func.date(GbifData.fetch_date).label('date'),
        func.count(GbifData.id).label('count')
    ).group_by(func.date(GbifData.fetch_date)).all()

    for date, count in date_counts:
        print(f"  {date}: {count} observations")

print("\n" + "=" * 60)
print("Check complete!")
print("=" * 60)
