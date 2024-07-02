import pytest
from dash.testing.application_runners import import_app

# Assuming your Dash app is defined in a file named 'app.py' and the app instance is named 'app'
app = import_app('app')

@pytest.fixture
def dash_duo(dash_duo):
    """Fixture to create a Dash test browser."""
    dash_duo.start_server(app)
    return dash_duo

def test_header_present(dash_duo):
    """Test that the header is present."""
    dash_duo.wait_for_element('h1', timeout=10)
    header = dash_duo.find_element('h1')
    assert header.text == "Sales Analysis Dashboard"

def test_visualisation_present(dash_duo):
    """Test that the visualisations are present."""
    dash_duo.wait_for_element('#individual-product-sales-bar-chart', timeout=10)
    dash_duo.wait_for_element('#total-sales-bar-chart', timeout=10)
    dash_duo.wait_for_element('#sales-over-time-line-chart', timeout=10)

def test_region_picker_present(dash_duo):
    """Test that the region picker (product dropdown) is present."""
    dash_duo.wait_for_element('#product-dropdown', timeout=10)
