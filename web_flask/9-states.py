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


@app.route('/states', strict_slashes=False)
def list_all_states():
    """
    It lists all the State objects present in DBStorage
    """
    states = storage.all(State).values()
    h1 = 'States'
    return render_template('9-states.html', states=states, heading=h1)


@app.route('/states/<id>', strict_slashes=False)
def list_state_by_id(id):
    """
    It lists a State object by Id present in DBStorage
    """
    state = storage.all(State).get('State.{}'.format(id))
    h1 = 'State: {}'.format(state.name) if state else 'Not found!'
    return render_template('9-states.html', states=state, heading=h1)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
