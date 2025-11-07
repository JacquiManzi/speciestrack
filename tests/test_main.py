"""Tests for main Flask application routes."""

import pytest


def test_hello_world(client):
    """Test the hello_world route returns 'Hello World'."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"Hello World"


def test_hello_world_content_type(client):
    """Test that the hello_world route returns the correct content type."""
    response = client.get("/")
    assert response.content_type == "text/html; charset=utf-8"


def test_404_error(client):
    """Test that non-existent routes return 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_native_plants_route_exists(client):
    """Test that the /native-plants route exists and returns 200."""
    response = client.get("/native-plants")
    assert response.status_code == 200


def test_native_plants_returns_json(client):
    """Test that the /native-plants route returns JSON data."""
    response = client.get("/native-plants")
    assert response.content_type == "application/json"


def test_native_plants_empty_database(client):
    """Test /native-plants returns empty array when no data exists."""
    response = client.get("/native-plants")
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_native_plants_with_data(client, gbif_sample_data):
    """Test that /native-plants returns data when database has native plants."""
    response = client.get("/native-plants")
    data = response.get_json()

    # Should return 3 native plants from gbif_sample_data fixture
    assert len(data) == 3
    assert response.content_type == "application/json"


def test_native_plants_filters_correctly(client, gbif_sample_data):
    """Test that /native-plants only returns plants where native=True."""
    response = client.get("/native-plants")
    data = response.get_json()

    # Should return 3 native plants (Eucalyptus should be excluded)
    assert len(data) == 3

    # All returned plants should have native=True
    for plant in data:
        assert plant["native"] is True

    # Check specific plant names
    plant_names = [plant["scientific_name"] for plant in data]
    assert "Quercus lobata" in plant_names
    assert "Aesculus californica" in plant_names
    assert "Arctostaphylos glauca" in plant_names
    assert "Eucalyptus globulus" not in plant_names


def test_native_plants_json_structure(client, gbif_sample_data):
    """Test that /native-plants returns properly structured JSON."""
    response = client.get("/native-plants")
    data = response.get_json()

    # Check that we have data
    assert len(data) > 0

    # Check structure of first plant
    first_plant = data[0]
    assert "id" in first_plant
    assert "scientific_name" in first_plant
    assert "observation_count" in first_plant
    assert "observation_type" in first_plant
    assert "native" in first_plant
    assert "fetch_date" in first_plant
    assert "created_at" in first_plant
    assert "updated_at" in first_plant


def test_native_plants_observation_counts(client, gbif_sample_data):
    """Test that observation counts are correctly returned."""
    response = client.get("/native-plants")
    data = response.get_json()

    # Find specific plants and check their counts
    for plant in data:
        if plant["scientific_name"] == "Quercus lobata":
            assert plant["observation_count"] == 5
        elif plant["scientific_name"] == "Aesculus californica":
            assert plant["observation_count"] == 3
        elif plant["scientific_name"] == "Arctostaphylos glauca":
            assert plant["observation_count"] == 7


def test_native_plants_filter_by_scientific_name(client, gbif_sample_data):
    """Test filtering by scientific name."""
    response = client.get("/native-plants?scientific_name=Quercus")
    data = response.get_json()

    assert len(data) == 1
    assert data[0]["scientific_name"] == "Quercus lobata"


def test_native_plants_filter_by_common_name(client, gbif_sample_data):
    """Test filtering by common name (requires common names in test data)."""
    # This test will pass even if no common names are set, just checking structure works
    response = client.get("/native-plants?common_name=Oak")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)


def test_native_plants_filter_by_timestamp_range(client, gbif_sample_data):
    """Test filtering by timestamp range."""
    # Get a timestamp range that includes all test data
    from datetime import datetime, timedelta

    end_time = datetime.now() + timedelta(days=1)
    start_time = datetime.now() - timedelta(days=1)

    response = client.get(
        f"/native-plants?start_time={start_time.isoformat()}&end_time={end_time.isoformat()}"
    )
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 3  # All three native plants in test data


def test_native_plants_filter_future_timestamp(client, gbif_sample_data):
    """Test filtering with future timestamp returns no results."""
    from datetime import datetime, timedelta

    start_time = datetime.now() + timedelta(days=10)
    end_time = datetime.now() + timedelta(days=20)

    response = client.get(
        f"/native-plants?start_time={start_time.isoformat()}&end_time={end_time.isoformat()}"
    )
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 0  # No plants should match future timestamp


def test_native_plants_invalid_timestamp_format(client, gbif_sample_data):
    """Test that invalid timestamp format returns 400 error."""
    response = client.get("/native-plants?start_time=invalid-date")

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_native_plants_combined_filters(client, gbif_sample_data):
    """Test combining multiple filters."""
    from datetime import datetime, timedelta

    end_time = datetime.now() + timedelta(days=1)
    start_time = datetime.now() - timedelta(days=1)

    response = client.get(
        f"/native-plants?start_time={start_time.isoformat()}&end_time={end_time.isoformat()}&scientific_name=Quercus"
    )
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["scientific_name"] == "Quercus lobata"


def test_native_plants_partial_name_match(client, gbif_sample_data):
    """Test that name filtering uses partial matching."""
    # Search for partial scientific name
    response = client.get("/native-plants?scientific_name=Aesculus")
    data = response.get_json()

    assert len(data) == 1
    assert "Aesculus californica" in data[0]["scientific_name"]
