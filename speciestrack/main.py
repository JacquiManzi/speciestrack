from flask import Flask
from speciestrack.controllers.map_controller import show_map

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/map')
def map_page():
    return show_map()

if __name__ == '__main__':

    app.run()