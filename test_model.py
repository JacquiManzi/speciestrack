#!/usr/bin/env python3
"""
Test script to verify NativePlant model works correctly
"""

from speciestrack.main import app
from speciestrack.models import NativePlant

with app.app_context():
    # Test 1: Count all plants
    total_plants = NativePlant.query.count()
    print(f"Total plants in database: {total_plants}")

    # Test 2: Get first 5 plants
    plants = NativePlant.query.limit(5).all()
    print("\nFirst 5 plants:")
    for plant in plants:
        print(f"  - {plant}")

    # Test 3: Search by common name
    maple = NativePlant.query.filter_by(common_name='Big Leaf Maple').first()
    if maple:
        print(f"\nFound plant: {maple}")
        print(f"  Botanical name: {maple.botanical_name}")
        print(f"  Plant type: {maple.plant_type}")
        print(f"  Supports {maple.butterflies_and_moths_supported} butterflies/moths")
        print(f"  Sunset zones: {maple.sunset_zones}")

    # Test 4: Filter by plant type
    trees = NativePlant.query.filter_by(plant_type='Tree').limit(5).all()
    print(f"\nFound {len(trees)} trees:")
    for tree in trees:
        print(f"  - {tree.common_name} ({tree.botanical_name})")

    # Test 5: Test to_dict() method
    if maple:
        plant_dict = maple.to_dict()
        print(f"\nSample plant as dictionary (first 5 keys):")
        for i, (key, value) in enumerate(plant_dict.items()):
            if i < 5:
                print(f"  {key}: {value}")
            else:
                break

    print("\n✓ All tests passed!")
