from flask import Flask
from speciestrack.controllers.map_controller import get_native_plants
from speciestrack.models import db, NativePlant, GbifData
from speciestrack.jobs.gbif_job import store_gbif_data
from apscheduler.schedulers.background import BackgroundScheduler
import os
import atexit

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://localhost/california_native_plants'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Configure scheduler for daily jobs
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=lambda: store_gbif_data(app),
    trigger="cron",
    hour=12,
    minute=0,
    id='gbif_daily_fetch',
    name='Fetch GBIF data daily at 12pm',
    replace_existing=True
)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route("/")
def hello_world():
    return "Hello World"

@app.route("/native-plants")
def native_plants():
    return get_native_plants()


if __name__ == "__main__":

    app.run()
