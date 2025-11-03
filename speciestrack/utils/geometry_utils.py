"""Utility functions for geometry processing."""


def simplify_polygon(coordinates, max_points=100):
    """
    Simplify a polygon by reducing the number of coordinate points.
    Uses a simple point reduction algorithm to keep approximately every nth point.

    Args:
        coordinates: List of (lon, lat) tuples
        max_points: Maximum number of points to keep

    Returns:
        List of simplified (lon, lat) tuples
    """
    if len(coordinates) <= max_points:
        return coordinates

    # Calculate step size to get approximately max_points
    step = len(coordinates) // max_points

    # Keep every nth point, but always keep first and last
    simplified = coordinates[::step]

    # Ensure first and last points are included
    if simplified[0] != coordinates[0]:
        simplified.insert(0, coordinates[0])
    if simplified[-1] != coordinates[-1]:
        simplified.append(coordinates[-1])

    return simplified


def create_wkt_polygon(coordinates, simplify=True, max_points=50):
    """
    Create a WKT POLYGON string from coordinates.

    Args:
        coordinates: List of (lon, lat) tuples
        simplify: Whether to simplify the polygon
        max_points: Maximum points if simplifying

    Returns:
        WKT POLYGON string formatted for GBIF API
    """
    if simplify:
        coordinates = simplify_polygon(coordinates, max_points)

    # Ensure polygon closes (first point = last point)
    if coordinates[0] != coordinates[-1]:
        coordinates.append(coordinates[0])

    # Format as "lon lat" pairs
    coord_strings = [f"{lon} {lat}" for lon, lat in coordinates]

    # Create WKT string with NO SPACES after POLYGON
    wkt = f"POLYGON(({','.join(coord_strings)}))"

    return wkt


def get_bounding_box_polygon(min_lon, min_lat, max_lon, max_lat):
    """
    Create a simple bounding box polygon from bounds.
    This is useful for testing or when a simple rectangular area is sufficient.

    Args:
        min_lon: Minimum longitude
        min_lat: Minimum latitude
        max_lon: Maximum longitude
        max_lat: Maximum latitude

    Returns:
        WKT POLYGON string for the bounding box
    """
    # Create anticlockwise box
    coordinates = [
        (min_lon, min_lat),
        (max_lon, min_lat),
        (max_lon, max_lat),
        (min_lon, max_lat),
        (min_lon, min_lat),  # Close the polygon
    ]

    coord_strings = [f"{lon} {lat}" for lon, lat in coordinates]
    return f"POLYGON(({','.join(coord_strings)}))"
