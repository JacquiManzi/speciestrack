#!/usr/bin/env python3
"""
Script to check common names in GBIF data.
"""

from speciestrack.main import app
from speciestrack.models import GbifData

print("=" * 60)
print("Checking Common Names in GBIF Data")
print("=" * 60)

with app.app_context():
    # Count entries with common names
    total_count = GbifData.query.count()
    with_common_name = GbifData.query.filter(GbifData.common_name.isnot(None)).count()
    without_common_name = GbifData.query.filter(GbifData.common_name.is_(None)).count()

    print(f"\nTotal observations: {total_count}")
    print(f"With common name: {with_common_name} ({with_common_name/total_count*100:.1f}%)")
    print(f"Without common name: {without_common_name} ({without_common_name/total_count*100:.1f}%)")

    # Show native plants with common names
    print("\n" + "=" * 60)
    print("Native Plants with Common Names (first 10)")
    print("=" * 60)
    native_with_names = GbifData.query.filter(
        GbifData.native == True,
        GbifData.common_name.isnot(None)
    ).limit(10).all()

    for plant in native_with_names:
        print(f"{plant.scientific_name:50} -> {plant.common_name}")

    # Show all entries with common names
    print("\n" + "=" * 60)
    print("All Entries with Common Names (first 20)")
    print("=" * 60)
    all_with_names = GbifData.query.filter(
        GbifData.common_name.isnot(None)
    ).limit(20).all()

    for entry in all_with_names:
        native_status = "NATIVE" if entry.native else "non-native"
        print(f"{entry.scientific_name:50} [{native_status:10}] -> {entry.common_name}")

print("\n" + "=" * 60)
print("Check complete!")
print("=" * 60)
