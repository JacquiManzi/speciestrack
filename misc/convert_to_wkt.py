import json

# Read the JSON file
with open("/Users/jacquimanzi/Downloads/export.json", "r") as f:
    data = json.load(f)

# Extract the relation element
relation = data["elements"][0]

# Separate outer and inner members
outer_coords = []
inner_coords = []

for member in relation["members"]:
    if "geometry" in member:
        if member["role"] == "outer":
            # Convert lat/lon to lon/lat and add to outer coordinates
            for point in member["geometry"]:
                outer_coords.append(f"{point['lon']} {point['lat']}")
        elif member["role"] == "inner":
            # Convert lat/lon to lon/lat and add to inner coordinates
            for point in member["geometry"]:
                inner_coords.append(f"{point['lon']} {point['lat']}")

# Ensure the polygon closes (first point = last point)
if outer_coords and outer_coords[0] != outer_coords[-1]:
    outer_coords.append(outer_coords[0])

if inner_coords and inner_coords[0] != inner_coords[-1]:
    inner_coords.append(inner_coords[0])

# Construct WKT POLYGON
outer_ring = ", ".join(outer_coords)

if inner_coords:
    inner_ring = ", ".join(inner_coords)
    wkt = f"POLYGON (({outer_ring}), ({inner_ring}))"
else:
    wkt = f"POLYGON (({outer_ring}))"

# Print the result
print("WKT Polygon:")
print(wkt)
print()
print(f"Total outer coordinates: {len(outer_coords)}")
print(f"Total inner coordinates: {len(inner_coords)}")

# Save to file
with open("/Users/jacquimanzi/code/speciestrack/polygon.wkt", "w") as f:
    f.write(wkt)

print("\nWKT saved to: /Users/jacquimanzi/code/speciestrack/polygon.wkt")
