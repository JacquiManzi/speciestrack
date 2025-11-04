"""Tests for GBIF data fetching and storage job."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from speciestrack.jobs.gbif_job import fetch_gbif_data_raw, store_gbif_data
from speciestrack.models.gbif_data import GbifData
from speciestrack.models.native_plant import NativePlant


class TestFetchGbifDataRaw:
    """Tests for fetch_gbif_data_raw function."""

    @patch('speciestrack.jobs.gbif_job.requests.get')
    def test_fetch_gbif_data_success(self, mock_get):
        """Test successful GBIF data fetch with single page."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {"scientificName": "Quercus lobata"},
                {"scientificName": "Aesculus californica"},
            ]
        }
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_gbif_data_raw()

        # Verify results
        assert len(result) == 2
        assert result[0]["name"] == "Quercus lobata"
        assert result[1]["name"] == "Aesculus californica"

    @patch('speciestrack.jobs.gbif_job.requests.get')
    def test_fetch_gbif_data_empty_results(self, mock_get):
        """Test GBIF data fetch with no results."""
        # Mock empty API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_gbif_data_raw()

        # Verify results
        assert len(result) == 0

    @patch('speciestrack.jobs.gbif_job.requests.get')
    def test_fetch_gbif_data_api_error(self, mock_get):
        """Test GBIF data fetch with API error."""
        # Mock failed API response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_gbif_data_raw()

        # Should return empty list on error
        assert len(result) == 0

    @patch('speciestrack.jobs.gbif_job.requests.get')
    def test_fetch_gbif_data_pagination(self, mock_get):
        """Test GBIF data fetch with pagination (multiple pages)."""
        # Mock two pages of results
        page1_response = Mock()
        page1_response.status_code = 200
        page1_response.json.return_value = {
            "results": [{"scientificName": f"Species {i}"} for i in range(300)]
        }

        page2_response = Mock()
        page2_response.status_code = 200
        page2_response.json.return_value = {
            "results": [{"scientificName": "Last species"}]
        }

        # Return different responses for each call
        mock_get.side_effect = [page1_response, page2_response]

        # Call the function
        result = fetch_gbif_data_raw()

        # Verify results from both pages
        assert len(result) == 301
        assert mock_get.call_count == 2

    @patch('speciestrack.jobs.gbif_job.requests.get')
    def test_fetch_gbif_data_filters_missing_names(self, mock_get):
        """Test that entries without scientificName are filtered out."""
        # Mock response with missing names
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {"scientificName": "Valid species"},
                {"commonName": "No scientific name"},
                {},
            ]
        }
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_gbif_data_raw()

        # Only the valid entry should be returned
        assert len(result) == 1
        assert result[0]["name"] == "Valid species"


class TestStoreGbifData:
    """Tests for store_gbif_data function."""

    @patch('speciestrack.jobs.gbif_job.fetch_gbif_data_raw')
    def test_store_gbif_data_success(self, mock_fetch, app, db):
        """Test successful storage of GBIF data."""
        # Mock fetch function to return test data
        mock_fetch.return_value = [
            {"name": "Test species 1", "type": "specimen", "count": 5},
            {"name": "Test species 2", "type": "observation", "count": 3},
        ]

        # Call the function
        store_gbif_data(app)

        # Verify data was stored
        stored_count = GbifData.query.count()
        assert stored_count == 2

        # Verify specific entries
        species1 = GbifData.query.filter_by(scientific_name="Test species 1").first()
        assert species1 is not None
        assert species1.observation_count == 5
        assert species1.observation_type == "specimen"

    @patch('speciestrack.jobs.gbif_job.fetch_gbif_data_raw')
    def test_store_gbif_data_empty_fetch(self, mock_fetch, app, db):
        """Test storage when fetch returns no data."""
        # Mock empty fetch
        mock_fetch.return_value = []

        # Call the function
        store_gbif_data(app)

        # Verify no data was stored
        stored_count = GbifData.query.count()
        assert stored_count == 0

    @patch('speciestrack.jobs.gbif_job.fetch_gbif_data_raw')
    def test_store_gbif_data_identifies_native_plants(self, mock_fetch, app, db, native_plant_sample_data):
        """Test that native plants are correctly identified."""
        # Mock fetch to return species that match native plants
        mock_fetch.return_value = [
            {"name": "Quercus lobata", "type": "specimen", "count": 1},
            {"name": "Eucalyptus globulus", "type": "specimen", "count": 1},
        ]

        # Call the function
        store_gbif_data(app)

        # Verify native flag is set correctly
        native_plant = GbifData.query.filter_by(scientific_name="Quercus lobata").first()
        assert native_plant is not None
        assert native_plant.native is True

        non_native_plant = GbifData.query.filter_by(scientific_name="Eucalyptus globulus").first()
        assert non_native_plant is not None
        assert non_native_plant.native is False

    @patch('speciestrack.jobs.gbif_job.fetch_gbif_data_raw')
    def test_store_gbif_data_matches_with_author_names(self, mock_fetch, app, db, native_plant_sample_data):
        """Test that species with author names are matched to native plants."""
        # Mock fetch with author names appended
        mock_fetch.return_value = [
            {"name": "Quercus lobata Née", "type": "specimen", "count": 1},
            {"name": "Aesculus californica (Spach) Nutt.", "type": "specimen", "count": 1},
        ]

        # Call the function
        store_gbif_data(app)

        # Verify native flag is set correctly even with author names
        species1 = GbifData.query.filter_by(scientific_name="Quercus lobata Née").first()
        assert species1 is not None
        assert species1.native is True

        species2 = GbifData.query.filter_by(scientific_name="Aesculus californica (Spach) Nutt.").first()
        assert species2 is not None
        assert species2.native is True

    @patch('speciestrack.jobs.gbif_job.fetch_gbif_data_raw')
    def test_store_gbif_data_sets_fetch_date(self, mock_fetch, app, db):
        """Test that fetch_date is set when storing data."""
        # Mock fetch
        mock_fetch.return_value = [
            {"name": "Test species", "type": "specimen", "count": 1},
        ]

        # Get time before calling
        before_time = datetime.now()

        # Call the function
        store_gbif_data(app)

        # Get time after calling
        after_time = datetime.now()

        # Verify fetch_date is set
        species = GbifData.query.first()
        assert species is not None
        assert species.fetch_date is not None
        assert before_time <= species.fetch_date <= after_time

    @patch('speciestrack.jobs.gbif_job.fetch_gbif_data_raw')
    def test_store_gbif_data_handles_errors_gracefully(self, mock_fetch, app, db):
        """Test that errors during storage are handled gracefully."""
        # Mock fetch to raise an exception
        mock_fetch.side_effect = Exception("API error")

        # Call the function - should not raise exception
        try:
            store_gbif_data(app)
        except Exception as e:
            pytest.fail(f"store_gbif_data raised an exception: {e}")

        # Verify no data was stored
        stored_count = GbifData.query.count()
        assert stored_count == 0

    @patch('speciestrack.jobs.gbif_job.fetch_gbif_data_raw')
    def test_store_gbif_data_handles_partial_errors(self, mock_fetch, app, db):
        """Test that individual entry errors don't stop the entire job."""
        # Mock fetch with valid and problematic data
        mock_fetch.return_value = [
            {"name": "Valid species", "type": "specimen", "count": 1},
            {"name": "", "type": "specimen", "count": 1},  # Empty name
            {"name": "Another valid species", "type": "observation", "count": 2},
        ]

        # Call the function
        store_gbif_data(app)

        # Verify valid entries were stored despite error in one entry
        stored_count = GbifData.query.count()
        assert stored_count >= 2  # At least the valid ones should be stored
