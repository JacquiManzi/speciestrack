#!/usr/bin/env python3
"""
Script to check what common names exist in native_plants table.
"""

from speciestrack.main import app
from speciestrack.models import NativePlant

print("=" * 60)
print("Checking Common Names in Native Plants Table")
print("=" * 60)

with app.app_context():
    # Get some native plants
    plants = NativePlant.query.limit(20).all()

    print(f"\nTotal native plants in database: {NativePlant.query.count()}")
    print("\nFirst 20 plants:")
    print("-" * 60)

    for plant in plants:
        print(f"Botanical: {plant.botanical_name:40}")
        print(f"Common:    {plant.common_name}")
        print(f"Type:      {type(plant.common_name)}")
        print("-" * 60)

print("\nDone!")
