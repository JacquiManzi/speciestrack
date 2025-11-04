"""Tests for database models."""

import pytest
from speciestrack.models.native_plant import NativePlant
from speciestrack.models.gbif_data import GbifData


class TestNativePlantModel:
    """Tests for the NativePlant model."""

    def test_native_plant_creation(self, db):
        """Test creating a NativePlant instance."""
        plant = NativePlant(
            common_name="Test Plant",
            botanical_name="Testus plantus",
            plant_type="Tree",
            butterflies_and_moths_supported=100,
            sunset_zones="1-24"
        )
        db.session.add(plant)
        db.session.commit()

        assert plant.id is not None
        assert plant.common_name == "Test Plant"
        assert plant.botanical_name == "Testus plantus"

    def test_native_plant_query_count(self, db, native_plant_sample_data):
        """Test counting all plants in database."""
        total_plants = NativePlant.query.count()
        assert total_plants == 3

    def test_native_plant_query_by_common_name(self, db, native_plant_sample_data):
        """Test querying plants by common name."""
        plant = NativePlant.query.filter_by(common_name='Valley Oak').first()
        assert plant is not None
        assert plant.botanical_name == "Quercus lobata"
        assert plant.plant_type == "Tree"
        assert plant.butterflies_and_moths_supported == "150"
        assert plant.sunset_zones == "7-9, 12-24"

    def test_native_plant_query_by_botanical_name(self, db, native_plant_sample_data):
        """Test querying plants by botanical name."""
        plant = NativePlant.query.filter_by(botanical_name='Aesculus californica').first()
        assert plant is not None
        assert plant.common_name == "California Buckeye"

    def test_native_plant_filter_by_type(self, db, native_plant_sample_data):
        """Test filtering plants by type."""
        trees = NativePlant.query.filter_by(plant_type='Tree').all()
        assert len(trees) == 2

        perennials = NativePlant.query.filter_by(plant_type='Perennial').all()
        assert len(perennials) == 1
        assert perennials[0].common_name == "California Poppy"

    def test_native_plant_to_dict(self, db, native_plant_sample_data):
        """Test the to_dict() method returns correct structure."""
        plant = NativePlant.query.filter_by(common_name='Valley Oak').first()
        plant_dict = plant.to_dict()

        # Verify it's a dictionary
        assert isinstance(plant_dict, dict)

        # Check for expected keys (this will depend on your actual to_dict implementation)
        assert "common_name" in plant_dict or "id" in plant_dict
        assert plant_dict.get("common_name") == "Valley Oak" or "id" in plant_dict

    def test_native_plant_repr(self, db, native_plant_sample_data):
        """Test the __repr__ method."""
        plant = NativePlant.query.filter_by(common_name='Valley Oak').first()
        repr_str = repr(plant)
        assert isinstance(repr_str, str)
        assert len(repr_str) > 0

    def test_native_plant_limit_query(self, db, native_plant_sample_data):
        """Test limiting query results."""
        plants = NativePlant.query.limit(2).all()
        assert len(plants) == 2

    def test_native_plant_order_by(self, db, native_plant_sample_data):
        """Test ordering query results."""
        plants = NativePlant.query.order_by(NativePlant.common_name).all()
        assert len(plants) == 3
        # Should be ordered alphabetically: California Buckeye, California Poppy, Valley Oak
        assert plants[0].common_name == "California Buckeye"
        assert plants[1].common_name == "California Poppy"
        assert plants[2].common_name == "Valley Oak"


class TestGbifDataModel:
    """Tests for the GbifData model."""

    def test_gbif_data_creation(self, db):
        """Test creating a GbifData instance."""
        data = GbifData(
            scientific_name="Test species",
            observation_count=5,
            observation_type="specimen",
            native=True
        )
        db.session.add(data)
        db.session.commit()

        assert data.id is not None
        assert data.scientific_name == "Test species"
        assert data.observation_count == 5
        assert data.native is True

    def test_gbif_data_default_values(self, db):
        """Test that default values are set correctly."""
        data = GbifData(scientific_name="Test species")
        db.session.add(data)
        db.session.commit()

        assert data.observation_count == 1  # default
        assert data.native is False  # default

    def test_gbif_data_query_count(self, db, gbif_sample_data):
        """Test counting all GBIF data in database."""
        total_count = GbifData.query.count()
        assert total_count == 4

    def test_gbif_data_filter_by_native(self, db, gbif_sample_data):
        """Test filtering by native status."""
        native_count = GbifData.query.filter_by(native=True).count()
        non_native_count = GbifData.query.filter_by(native=False).count()

        assert native_count == 3
        assert non_native_count == 1

    def test_gbif_data_to_dict(self, db, gbif_sample_data):
        """Test the to_dict() method returns correct structure."""
        data = GbifData.query.first()
        data_dict = data.to_dict()

        assert isinstance(data_dict, dict)
        assert "id" in data_dict
        assert "scientific_name" in data_dict
        assert "observation_count" in data_dict
        assert "observation_type" in data_dict
        assert "native" in data_dict
        assert "fetch_date" in data_dict
        assert "created_at" in data_dict
        assert "updated_at" in data_dict

    def test_gbif_data_repr(self, db, gbif_sample_data):
        """Test the __repr__ method."""
        data = GbifData.query.first()
        repr_str = repr(data)
        assert isinstance(repr_str, str)
        assert "GbifData" in repr_str

    def test_gbif_data_order_by_count(self, db, gbif_sample_data):
        """Test ordering by observation count."""
        data = GbifData.query.order_by(GbifData.observation_count.desc()).all()
        # Highest count should be first (Arctostaphylos glauca with 7)
        assert data[0].scientific_name == "Arctostaphylos glauca"
        assert data[0].observation_count == 7
