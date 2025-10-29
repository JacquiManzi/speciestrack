import pytest
from speciestrack.main import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_hello_world(client):
    """Test the hello_world route returns 'Hello World'."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Hello World'


def test_hello_world_content_type(client):
    """Test that the hello_world route returns the correct content type."""
    response = client.get('/')
    assert response.content_type == 'text/html; charset=utf-8'


def test_404_error(client):
    """Test that non-existent routes return 404."""
    response = client.get('/nonexistent')
    assert response.status_code == 404


def test_map_route_exists(client):
    """Test that the /map route exists and returns 200."""
    response = client.get('/map')
    assert response.status_code == 200


def test_map_route_content(client):
    """Test that the /map route returns expected content."""
    response = client.get('/map')
    assert b'Species Map' in response.data
    assert b'Track native and invasive species' in response.data


def test_map_route_species_data(client):
    """Test that the /map route displays species data."""
    response = client.get('/map')
    # Check for example species from the controller
    assert b'Bald Eagle' in response.data
    assert b'European Starling' in response.data
    assert b'Red-tailed Hawk' in response.data


def test_map_route_species_types(client):
    """Test that the /map route displays native and invasive labels."""
    response = client.get('/map')
    assert b'NATIVE' in response.data
    assert b'INVASIVE' in response.data
