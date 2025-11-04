#!/usr/bin/env python3
"""
View all scheduled jobs and their next run times
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import speciestrack
sys.path.insert(0, str(Path(__file__).parent.parent))

from speciestrack.main import app, scheduler
from datetime import datetime

print("=" * 70)
print("Scheduled Jobs Status")
print("=" * 70)
print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Scheduler running: {scheduler.running}")
print("=" * 70)

jobs = scheduler.get_jobs()

if not jobs:
    print("\nNo scheduled jobs found.")
else:
    print(f"\nTotal jobs: {len(jobs)}\n")
    for job in jobs:
        print(f"Job ID: {job.id}")
        print(f"Name: {job.name}")
        print(f"Next run: {job.next_run_time}")
        print(f"Trigger: {job.trigger}")
        print("-" * 70)

print("\nTo stop the scheduler, exit the Flask application.")
print("=" * 70)
