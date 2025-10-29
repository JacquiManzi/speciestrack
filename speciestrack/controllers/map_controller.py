from flask import render_template


def show_map():
    """
    Controller for the map page.
    Renders the map view with species tracking data.
    """
   
    species_data = [
        {'name': 'Bald Eagle', 'type': 'native', 'count': 15},
        {'name': 'European Starling', 'type': 'invasive', 'count': 47},
        {'name': 'Red-tailed Hawk', 'type': 'native', 'count': 8},
    ]

    return render_template('map.html', species=species_data, title='Species Map')
