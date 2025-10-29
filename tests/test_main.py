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
