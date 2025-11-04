"""
Scheduled job to fetch and store GBIF data daily
"""

from datetime import datetime
from dotenv import load_dotenv
from speciestrack.models import db, GbifData, NativePlant
from speciestrack.utils.date_utils import get_date_json
import requests
import os

load_dotenv()


def fetch_gbif_data_raw():
    """
    Fetch occurrence data from GBIF API and return raw data.
    This is a non-Flask version for use in scheduled jobs.
    Paginates through all results using limit and offset.
    """
    url = os.getenv("GBIF_API_URL")
    username = os.getenv("GBIF_USERNAME")
    password = os.getenv("GBIF_PASSWORD")
    date_info = get_date_json()

    # Constants for pagination
    LIMIT = 300  # Maximum allowed by GBIF API
    MAX_OFFSET = 100000  # Maximum offset allowed by GBIF API

    all_species_data = []
    offset = 0

    # Using bounding box from Wildcat Canyon Regional Park
    base_params = {
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

    print(f"Starting pagination: limit={LIMIT}, max_offset={MAX_OFFSET}")

    try:
        while offset <= MAX_OFFSET:
            # Add pagination parameters
            params = base_params.copy()
            params["limit"] = LIMIT
            params["offset"] = offset

            print(f"Fetching page at offset {offset}...")

            response = requests.get(url, params=params, auth=(username, password), timeout=30)

            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])

                # If no results, we've reached the end
                if not results:
                    print(f"No more results at offset {offset}. Pagination complete.")
                    break

                # Process results
                page_count = 0
                for item in results:
                    name = item.get("scientificName")
                    if name:
                        all_species_data.append({"name": name, "type": "", "count": 1})
                        page_count += 1

                print(f"Fetched {page_count} observations from offset {offset}")

                # If we got fewer results than the limit, we've reached the end
                if len(results) < LIMIT:
                    print(f"Received {len(results)} results (less than limit of {LIMIT}). Pagination complete.")
                    break

                # Move to next page
                offset += LIMIT

            else:
                print(f"Error fetching data from GBIF API at offset {offset}: {response.status_code} - {response.text}")
                break

        print(f"Pagination finished. Total observations fetched: {len(all_species_data)}")
        return all_species_data

    except Exception as e:
        print(f"Exception while fetching GBIF data: {e}")
        return all_species_data  # Return what we've collected so far


def store_gbif_data(app):
    """
    Scheduled job function to fetch and store GBIF data.
    Runs daily at 12pm.
    """
    with app.app_context():
        print(f"[{datetime.now()}] Starting GBIF data fetch job...")

        try:
            # Fetch data from GBIF API
            species_data = fetch_gbif_data_raw()

            if not species_data:
                print("No species data retrieved from GBIF API")
                return

            # Store each observation in the database
            stored_count = 0
            native_count = 0
            fetch_time = datetime.now()

            for item in species_data:
                try:
                    scientific_name = item.get("name", "")

                    # Check if this species is in the native_plants table
                    # GBIF includes author names (e.g. "Artemisia californica Less.")
                    # while native_plants table has just the species name
                    # We check if the GBIF name starts with any botanical_name from native_plants

                    # First try exact match
                    native_plant = NativePlant.query.filter_by(botanical_name=scientific_name).first()

                    # If no exact match, check if GBIF name starts with a native plant name + space
                    # This handles the case where GBIF has "Species name Author" and we have "Species name"
                    if not native_plant:
                        # Extract just genus and species (first two words) from GBIF name
                        words = scientific_name.split()
                        if len(words) >= 2:
                            genus_species = f"{words[0]} {words[1]}"
                            native_plant = NativePlant.query.filter(
                                NativePlant.botanical_name.like(f"{genus_species}%")
                            ).first()

                    # Determine if native and get common name
                    is_native = native_plant is not None
                    common_name = native_plant.common_name if native_plant is not None else None

                    gbif_entry = GbifData(
                        scientific_name=scientific_name,
                        common_name=common_name,
                        observation_count=item.get("count", 1),
                        observation_type=item.get("type", ""),
                        native=is_native,
                        fetch_date=fetch_time
                    )
                    db.session.add(gbif_entry)
                    stored_count += 1

                    if is_native:
                        native_count += 1

                except Exception as e:
                    print(f"Error storing entry for {item.get('name')}: {e}")
                    continue

            # Commit all entries
            db.session.commit()
            print(f"[{datetime.now()}] Successfully stored {stored_count} GBIF observations")
            print(f"[{datetime.now()}] Native plants found: {native_count} ({native_count/stored_count*100:.1f}%)")

        except Exception as e:
            print(f"Error in GBIF data job: {e}")
            db.session.rollback()
        finally:
            db.session.close()
