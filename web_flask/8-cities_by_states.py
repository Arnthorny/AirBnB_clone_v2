#!/usr/bin/python3
"""
Flask web application:

Your web application must be listening on 0.0.0.0, port 5000
Routes:
    /cities_by_states: display a HTML page: (inside the tag BODY)
"""
from flask import Flask, render_template
from models import State, storage


app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception=None):
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def list_cities():
    """
    It lists all the City objects present in DBStorage and their states
    """
    states = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
