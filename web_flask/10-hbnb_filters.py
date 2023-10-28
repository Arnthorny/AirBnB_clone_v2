#!/usr/bin/python3
"""
Flask web application:

Your web application must be listening on 0.0.0.0, port 5000
Routes:
    /cities_by_states: display a HTML page: (inside the tag BODY)
"""
from flask import Flask, render_template, url_for
from models import State, storage, Amenity


app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception=None):
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def render_entire_page():
    """
    It renders an entire page for the site
    """
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    return render_template('10-hbnb_filters.html',
                           states=states, amenities=amenities)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
