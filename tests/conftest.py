"""
Shared pytest fixtures for all tests.
This file provides common test setup including database configuration and fixtures.
"""

import pytest
from speciestrack.main import app as flask_app
from speciestrack.models import db as _db
from speciestrack.models.gbif_data import GbifData
from speciestrack.models.native_plant import NativePlant


@pytest.fixture(scope='function')
def app():
    """
    Create and configure a Flask app instance for testing.
    Uses an in-memory SQLite database instead of production PostgreSQL.
    """
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    # Create application context
    with flask_app.app_context():
        # Create all tables
        _db.create_all()

        yield flask_app

        # Cleanup
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='function')
def db(app):
    """
    Provide the database instance with tables created.
    Tables are dropped after each test.
    """
    return _db


@pytest.fixture(scope='function')
def client(app):
    """
    Create a test client for making HTTP requests to the Flask app.
    """
    return app.test_client()


@pytest.fixture(scope='function')
def gbif_sample_data(db):
    """
    Create sample GBIF data for testing.
    Returns a list of created GbifData objects.
    """
    native_plant1 = GbifData(
        scientific_name="Quercus lobata",
        occurrence_id="4055379494",
        observation_count=5,
        observation_type="specimen",
        native=True,
        decimal_latitude=37.9187,
        decimal_longitude=-122.3244
    )
    native_plant2 = GbifData(
        scientific_name="Aesculus californica",
        occurrence_id="4055379495",
        observation_count=3,
        observation_type="observation",
        native=True,
        decimal_latitude=37.9250,
        decimal_longitude=-122.2800
    )
    native_plant3 = GbifData(
        scientific_name="Arctostaphylos glauca",
        occurrence_id="4055379496",
        observation_count=7,
        observation_type="observation",
        native=True,
        decimal_latitude=37.9300,
        decimal_longitude=-122.2900
    )
    non_native_plant = GbifData(
        scientific_name="Eucalyptus globulus",
        occurrence_id="4055379497",
        observation_count=2,
        observation_type="specimen",
        native=False,
        decimal_latitude=37.9400,
        decimal_longitude=-122.3000
    )

    db.session.add_all([native_plant1, native_plant2, native_plant3, non_native_plant])
    db.session.commit()

    return [native_plant1, native_plant2, native_plant3, non_native_plant]


@pytest.fixture(scope='function')
def native_plant_sample_data(db):
    """
    Create sample NativePlant data for testing.
    Returns a list of created NativePlant objects.
    """
    plant1 = NativePlant(
        common_name="Valley Oak",
        botanical_name="Quercus lobata",
        plant_type="Tree",
        butterflies_and_moths_supported="150",
        sunset_zones="7-9, 12-24"
    )
    plant2 = NativePlant(
        common_name="California Buckeye",
        botanical_name="Aesculus californica",
        plant_type="Tree",
        butterflies_and_moths_supported="45",
        sunset_zones="4-10, 12-24"
    )
    plant3 = NativePlant(
        common_name="California Poppy",
        botanical_name="Eschscholzia californica",
        plant_type="Perennial",
        butterflies_and_moths_supported="20",
        sunset_zones="1-24"
    )

    db.session.add_all([plant1, plant2, plant3])
    db.session.commit()

    return [plant1, plant2, plant3]
