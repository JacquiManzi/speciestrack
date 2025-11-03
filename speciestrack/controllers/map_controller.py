from flask import jsonify
from dotenv import load_dotenv
from speciestrack.utils.date_utils import get_date_json

import requests
import os

load_dotenv()


def get_gbif_data():
    """
    Fetch occurrence data from GBIF API using provided parameters and authentication.
    """
    url = os.getenv("GBIF_API_URL")
    username = os.getenv("GBIF_USERNAME")
    password = os.getenv("GBIF_PASSWORD")
    date_info = get_date_json()

    # Using bounding box from Wildcat Canyon Regional Park
    params = {
        "dataset_key": os.getenv("DATASET_KEY"),
        "has_coordinate": "true",
        "has_geospatial_issue": "false",
        "state_province": "California",
        "advanced": "1",
        #"start_day_of_year": date_info["day"],
        #"month": date_info["month"],
        "year": date_info["year"],
        "geometry": "POLYGON((-122.28112 37.91874,-122.27067 37.92392,-122.27061 37.92138,-122.26765 37.92143,-122.262 37.92416,-122.2659 37.93392,-122.27042 37.93614,-122.28178 37.94702,-122.28391 37.9473,-122.28559 37.95072,-122.29028 37.95304,-122.28642 37.95197,-122.28435 37.95408,-122.29229 37.95429,-122.2975 37.95679,-122.29822 37.95575,-122.29613 37.95525,-122.29899 37.95366,-122.30203 37.95487,-122.30175 37.95264,-122.30828 37.95267,-122.30794 37.96,-122.31055 37.96004,-122.31557 37.9594,-122.31875 37.95404,-122.3244 37.95385,-122.32226 37.95131,-122.3163 37.95097,-122.31596 37.94868,-122.3138 37.94836,-122.31248 37.94682,-122.31136 37.94882,-122.30721 37.9454,-122.31131 37.9456,-122.31168 37.94403,-122.3101 37.94503,-122.29522 37.93138,-122.29224 37.93069,-122.29064 37.92924,-122.2918 37.92726,-122.28112 37.91874),(-122.31321 37.95783,-122.31039 37.95636,-122.31337 37.95701,-122.31321 37.95783))",
    }

    response = requests.get(url, params=params, auth=(username, password))
    if response.status_code == 200:
        print(f"response: {response.text}")

        data = response.json()
        species_data = []
        for item in data.get("results", []):
            name = item.get("scientificName")
            if name:
                species_data.append({"name": name, "type": "", "count": 1})
        return jsonify(species_data)
    else:
        print(f"Error fetching data from GBIF API: {response.text}")
        return response.raise_for_status()

