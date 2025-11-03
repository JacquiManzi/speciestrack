from flask import Flask
from speciestrack.controllers.map_controller import get_gbif_data

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World"


@app.route("/map")
def gbif_data():
    return get_gbif_data()


if __name__ == "__main__":

    app.run()
