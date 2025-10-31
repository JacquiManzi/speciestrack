"""Test script to verify the geometry string is correct."""

from speciestrack.utils.geometry_utils import get_bounding_box_polygon

# Wildcat Canyon Regional Park bounds from export.json
min_lon = -122.3244358
min_lat = 37.9187401
max_lon = -122.261997
max_lat = 37.960035

# Generate the polygon
geometry = get_bounding_box_polygon(min_lon, min_lat, max_lon, max_lat)

print("Generated Geometry String:")
print(geometry)
print()
print("Key characteristics:")
print(f"- Length: {len(geometry)} characters")
print(f"- Starts with 'POLYGON((': {geometry.startswith('POLYGON((')}")
print(f"- Ends with '))': {geometry.endswith('))')}")
print(f"- Number of coordinate pairs: {geometry.count(',') + 1}")
print()
print("This is a simple bounding box with 5 points (4 corners + closing point)")
print("which should be accepted by the GBIF API.")
