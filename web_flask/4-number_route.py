#!/usr/bin/python3
"""
Flask web application:

Your web application must be listening on 0.0.0.0, port 5000
Routes:
    /: display “Hello HBNB!”
    /hbnb: display “HBNB”
    /c/<text>: display “C ” followed by the value of the text variable.
"""
from flask import Flask, abort


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """
    This function defines what is to be returned by the given route
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hello_hbnb():
    """
    This function defines what is to be returned by the given route
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_variable(text):
    """
    This function defines what is to be returned by the given route
    It works with variable rules: Marking URL sections with tags <>
    """
    return 'C {}'.format(text.replace("_", " "))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_variable(text="is cool"):
    """
    This function defines what is to be returned by the given route
    It works with variable rules: Marking URL sections with tags <>
    """
    return 'Python {}'.format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def number_variable(n):
    """
    This function defines what is to be returned by the given route
    Display “n is a number” only if n is an integer
    """
    return '{} is a number'.format(n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
