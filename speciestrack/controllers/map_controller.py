from flask import jsonify, request
from speciestrack.models.gbif_data import GbifData
from datetime import datetime


def get_native_plants():
    """
    Query the gbif_data table for all native plants (native=True)
    and return as JSON response.

    Query Parameters:
        start_time (str): ISO format timestamp for start of time range
        end_time (str): ISO format timestamp for end of time range
        common_name (str): Filter by common name (partial match)
        scientific_name (str): Filter by scientific name (partial match)

    Example:
        /native-plants?start_time=2025-01-01T00:00:00&end_time=2025-12-31T23:59:59
        /native-plants?common_name=Oak
        /native-plants?scientific_name=Quercus
    """
    # Start with base query for native plants
    query = GbifData.query.filter_by(native=True)

    # Filter by timestamp range if provided
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if start_time:
        try:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            query = query.filter(GbifData.event_date >= start_dt)
        except (ValueError, AttributeError) as e:
            return jsonify({"error": f"Invalid start_time format: {str(e)}"}), 400

    if end_time:
        try:
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            query = query.filter(GbifData.event_date <= end_dt)
        except (ValueError, AttributeError) as e:
            return jsonify({"error": f"Invalid end_time format: {str(e)}"}), 400

    # Filter by common name if provided
    common_name = request.args.get('common_name')
    if common_name:
        query = query.filter(GbifData.common_name.ilike(f'%{common_name}%'))

    # Filter by scientific name if provided
    scientific_name = request.args.get('scientific_name')
    if scientific_name:
        query = query.filter(GbifData.scientific_name.ilike(f'%{scientific_name}%'))

    # Execute query and return results
    native_plants = query.all()
    plants_data = [plant.to_dict() for plant in native_plants]
    return jsonify(plants_data)

