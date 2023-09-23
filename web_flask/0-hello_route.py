"""
Flask Web Application Documentation
"""

# Import the Flask module
from flask import Flask

# Create a Flask web application instance
app = Flask(__name__)

# Define a route for the root URL ("/") with the strict_slashes option set to False
@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Route Handler: hello_hbnb

    This function is the handler for the root URL ("/"). When a user accesses
    the root URL, it returns a simple "Hello HBNB!" message.

    :return: A string message, "Hello HBNB!"
    """
    return "Hello HBNB!"

# Entry point to run the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

