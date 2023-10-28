#!/usr/bin/python3
"""
Flask web application:

Your web application must be listening on 0.0.0.0, port 5000
Routes:
    /hbnb: display a HTML page like 8-index.html
"""
from flask import Flask, render_template, url_for
from models import State, storage, Amenity, User, Place


app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception=None):
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def render_entire_page():
    """
    It renders an entire page for the site
    """
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    users = storage.all(User)
    print(users)
    return render_template('100-hbnb.html', states=states, amenities=amenities,
                           places=places, users=users)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
