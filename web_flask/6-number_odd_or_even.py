#!/usr/bin/python3
"""starts a Flask web application"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Displays message"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays message"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """Displays C followed by value of the text"""
    text = text.replace("_", " ")
    return "C {}".format(text)


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    """Displays Python followed by value of the text"""
    text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Displays n is a number if n is int"""
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Displays HTML page if n is int"""
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """Displays HTML page if n is int"""
    return render_template('6-number_odd_or_even.html', number=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
