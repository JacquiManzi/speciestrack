# GBIF Data Collection Job

## Overview
This system automatically fetches species observation data from GBIF (Global Biodiversity Information Facility) and stores it in the database daily.

## Schedule
- **Frequency**: Daily
- **Time**: 12:00 PM (noon)
- **Timezone**: Local system time

## How It Works

### 1. Database Table
The `gbif_data` table stores observations with the following structure:
- `id` - Primary key
- `scientific_name` - Species scientific name
- `observation_count` - Number of observations (default: 1)
- `observation_type` - Type of observation (currently empty)
- `fetch_date` - When this data was fetched
- `created_at` - Record creation timestamp
- `updated_at` - Record update timestamp

### 2. Job Flow
1. Job triggers daily at 12pm
2. Calls `fetch_gbif_data_raw()` to retrieve data from GBIF API
3. Parses the response for species observations
4. Creates `GbifData` entries for each observation
5. Commits all entries to database
6. Logs success/failure

### 3. Files Created

#### Models
- `/speciestrack/models/gbif_data.py` - GbifData SQLAlchemy model

#### Jobs
- `/speciestrack/jobs/gbif_job.py` - Job functions:
  - `fetch_gbif_data_raw()` - Fetches data from GBIF API
  - `store_gbif_data(app)` - Main job function that stores data

#### Database
- `create_gbif_data_table.sql` - SQL schema for gbif_data table

#### Configuration
- Updated `/speciestrack/main.py` to configure APScheduler

## Testing

### Manual Job Execution
Run the job manually to test:
```bash
python test_gbif_job.py
```

This will:
1. Run the job immediately
2. Display stored observations
3. Show statistics by fetch date

### Query the Data
```bash
# Connect to database
export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"
psql -d california_native_plants

# View recent observations
SELECT * FROM gbif_data ORDER BY fetch_date DESC LIMIT 10;

# Count observations by date
SELECT DATE(fetch_date) as date, COUNT(*) as observations
FROM gbif_data
GROUP BY DATE(fetch_date)
ORDER BY date DESC;
```

## Using the Model in Code

```python
from speciestrack.main import app
from speciestrack.models import GbifData

with app.app_context():
    # Get all observations from today
    from datetime import date
    today_obs = GbifData.query.filter(
        func.date(GbifData.fetch_date) == date.today()
    ).all()

    # Find specific species
    species = GbifData.query.filter_by(
        scientific_name='Artemisia californica Less.'
    ).all()

    # Convert to JSON
    data = [obs.to_dict() for obs in today_obs]
```

## Dependencies
- APScheduler==3.10.4
- Flask-SQLAlchemy==3.1.1
- psycopg2-binary==2.9.11

## Monitoring
The job logs output to stdout:
- `[timestamp] Starting GBIF data fetch job...`
- `[timestamp] Successfully stored X GBIF observations`
- Error messages if any issues occur

## Environment Variables Required
- `GBIF_API_URL` - GBIF API endpoint
- `GBIF_USERNAME` - GBIF authentication username
- `GBIF_PASSWORD` - GBIF authentication password
- `DATASET_KEY` - GBIF dataset key

These should be configured in your `.env` file.
