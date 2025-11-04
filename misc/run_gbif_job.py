#!/usr/bin/env python3
"""
Script to manually run the GBIF data fetch and store job.
"""

from speciestrack.main import app
from speciestrack.jobs.gbif_job import store_gbif_data

print("=" * 60)
print("Running GBIF Data Fetch Job")
print("=" * 60)

# Run the job
store_gbif_data(app)

print("\n" + "=" * 60)
print("Job execution complete!")
print("=" * 60)
