from flask import jsonify
from speciestrack.models.gbif_data import GbifData

def get_native_plants():
    """
    Query the gbif_data table for all native plants (native=True)
    and return as JSON response.
    """
    native_plants = GbifData.query.filter_by(native=True).all()
    plants_data = [plant.to_dict() for plant in native_plants]
    return jsonify(plants_data)

