#!/usr/bin/python3
"""
Flask web application:

Your web application must be listening on 0.0.0.0, port 5000
    /states_list: display a HTML page: (inside the tag BODY)
            H1 tag: “States”
            UL tag: with the list of all State objects present
            in DBStorage sorted by name (A->Z) tip
            LI tag: description of one State: <state.id>: <B><state.name></B>
"""
from flask import Flask, render_template
from models import State, storage


app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception=None):
    storage.close()


@app.route('/states_list', strict_slashes=False)
def list_states():
    """
    This function defines what is to be returned by the given route
    It lists all the State objets present in DBStorage
    """
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
