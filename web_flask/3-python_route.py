#!/usr/bin/python3
"""
Flask Web Application Documentation
"""

# Import the Flask module
from flask import Flask, escape

# Create a Flask web application instance
app = Flask(__name__)


# Define a route for the root URL ("/") with the strict_slashes to False
@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Route Handler: hello_hbnb

    This function is the handler for the root URL ("/"). When a user accesses
    the root URL, it returns a simple "Hello HBNB!" message.

    :return: A string message, "Hello HBNB!"
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Handle root = hbnb
    when a clent acces the root it returns a message "HBNB"

    :return: A message string "HBNB
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def text(text):
    """
    Handle root = text
    when a clent acces the root it returns a message "HBNB"

    :return: A message string "{text}"
    """
    text = escape(text).replace('_', ' ')
    return f"C {text}"


@app.route('/python/<text>', strict_slashes=False)
def text(text):
    """
    Handle root = text
    when a clent acces the root it returns a message "{text}"
    or {default_msg} if there's no

    :return: A message string "{text}"
    """
    text = escape(text).replace(' ', '_')
    default_msg = "is cool"
    if not text:
        return f"Python {default_msg}"
    else:
        return f"Python {text}"


# Entry point to run the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
