"""Tests for geometry utility functions."""

import pytest
from speciestrack.utils.geometry_utils import (
    simplify_polygon,
    create_wkt_polygon,
    get_bounding_box_polygon
)


class TestSimplifyPolygon:
    """Tests for simplify_polygon function."""

    def test_simplify_polygon_with_large_input(self):
        """Test that simplify_polygon reduces points when input exceeds max_points."""
        # Create a large list of coordinates
        coordinates = [(i, i * 2) for i in range(200)]

        # Simplify to 50 points
        result = simplify_polygon(coordinates, max_points=50)

        # Result should have significantly fewer points than original
        # Note: May be slightly more than max_points due to endpoint preservation
        assert len(result) <= 52  # Allow small buffer for endpoint insertion
        assert len(result) < len(coordinates)  # But definitely fewer than original
        # First and last points should be preserved
        assert result[0] == coordinates[0]
        assert result[-1] == coordinates[-1]

    def test_simplify_polygon_with_small_input(self):
        """Test that simplify_polygon doesn't reduce points when input is already small."""
        coordinates = [(i, i * 2) for i in range(30)]

        # Try to simplify to 50 points (more than we have)
        result = simplify_polygon(coordinates, max_points=50)

        # Result should be unchanged
        assert len(result) == len(coordinates)
        assert result == coordinates

    def test_simplify_polygon_preserves_endpoints(self):
        """Test that first and last points are always preserved."""
        coordinates = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]

        result = simplify_polygon(coordinates, max_points=3)

        # First and last should match original
        assert result[0] == (0, 0)
        assert result[-1] == (5, 5)


class TestCreateWktPolygon:
    """Tests for create_wkt_polygon function."""

    def test_create_wkt_polygon_basic(self):
        """Test basic WKT polygon creation."""
        coordinates = [(0, 0), (1, 0), (1, 1), (0, 1)]

        result = create_wkt_polygon(coordinates, simplify=False)

        # Should start with POLYGON((
        assert result.startswith("POLYGON((")
        # Should end with ))
        assert result.endswith("))")
        # Should contain coordinates
        assert "0 0" in result
        assert "1 1" in result

    def test_create_wkt_polygon_closes_automatically(self):
        """Test that polygon is automatically closed if not already."""
        coordinates = [(0, 0), (1, 0), (1, 1), (0, 1)]

        result = create_wkt_polygon(coordinates, simplify=False)

        # The first coordinate should appear twice (start and end)
        coord_count = result.count("0 0")
        assert coord_count == 2  # Once at start, once at end (closing)

    def test_create_wkt_polygon_already_closed(self):
        """Test with polygon that's already closed."""
        coordinates = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]

        result = create_wkt_polygon(coordinates, simplify=False)

        assert result.startswith("POLYGON((")
        assert result.endswith("))")

    def test_create_wkt_polygon_with_simplification(self):
        """Test WKT creation with simplification enabled."""
        # Create many points
        coordinates = [(i, i * 2) for i in range(200)]

        result = create_wkt_polygon(coordinates, simplify=True, max_points=10)

        # Should still be valid WKT
        assert result.startswith("POLYGON((")
        assert result.endswith("))")
        # Should have fewer coordinates than original
        coord_pairs = result.count(",") + 1  # commas + 1 = number of coordinate pairs
        assert coord_pairs <= 15  # Account for closing point

    def test_create_wkt_polygon_format(self):
        """Test that WKT format matches GBIF requirements."""
        coordinates = [(0, 0), (1, 0), (1, 1), (0, 1)]

        result = create_wkt_polygon(coordinates, simplify=False)

        # No space after POLYGON
        assert result.startswith("POLYGON((") and not result.startswith("POLYGON ((")
        # Coordinates should be comma-separated
        assert "," in result
        # Each coordinate pair should have space between lon and lat
        assert "0 0" in result


class TestGetBoundingBoxPolygon:
    """Tests for get_bounding_box_polygon function."""

    def test_get_bounding_box_polygon_basic(self):
        """Test basic bounding box creation."""
        min_lon, min_lat = -122.5, 37.5
        max_lon, max_lat = -122.0, 38.0

        result = get_bounding_box_polygon(min_lon, min_lat, max_lon, max_lat)

        # Should be valid WKT
        assert result.startswith("POLYGON((")
        assert result.endswith("))")
        # Should contain all corner coordinates
        assert str(min_lon) in result
        assert str(min_lat) in result
        assert str(max_lon) in result
        assert str(max_lat) in result

    def test_get_bounding_box_polygon_is_closed(self):
        """Test that bounding box is automatically closed."""
        result = get_bounding_box_polygon(-122.5, 37.5, -122.0, 38.0)

        # First coordinate pair should appear twice
        # Extract first coordinate pair
        inner = result.replace("POLYGON((", "").replace("))", "")
        coords = inner.split(",")
        first_coord = coords[0]
        last_coord = coords[-1]

        assert first_coord == last_coord

    def test_get_bounding_box_polygon_format(self):
        """Test that bounding box follows correct WKT format."""
        result = get_bounding_box_polygon(-122.5, 37.5, -122.0, 38.0)

        # Should have exactly 5 coordinate pairs (4 corners + closing point)
        coord_count = result.count(",") + 1
        assert coord_count == 5

        # No space after POLYGON
        assert not result.startswith("POLYGON ((")

    def test_get_bounding_box_wildcat_canyon(self):
        """Test with actual Wildcat Canyon Regional Park bounds."""
        # Values from the original test_geometry.py
        min_lon = -122.3244358
        min_lat = 37.9187401
        max_lon = -122.261997
        max_lat = 37.960035

        result = get_bounding_box_polygon(min_lon, min_lat, max_lon, max_lat)

        # Verify it's valid WKT
        assert result.startswith("POLYGON((")
        assert result.endswith("))")

        # Verify length is reasonable (not too long)
        assert len(result) < 500  # Should be a simple bounding box

        # Verify number of coordinate pairs
        coord_count = result.count(",") + 1
        assert coord_count == 5  # 4 corners + closing point

    def test_get_bounding_box_negative_coordinates(self):
        """Test with negative coordinates (like Western hemisphere)."""
        result = get_bounding_box_polygon(-180, -90, -170, -80)

        assert result.startswith("POLYGON((")
        assert "-180" in result
        assert "-90" in result

    def test_get_bounding_box_positive_coordinates(self):
        """Test with positive coordinates (like Eastern hemisphere)."""
        result = get_bounding_box_polygon(0, 0, 10, 10)

        assert result.startswith("POLYGON((")
        # Check that coordinates are in result
        inner = result.replace("POLYGON((", "").replace("))", "")
        assert "0 0" in inner
        assert "10 10" in inner
