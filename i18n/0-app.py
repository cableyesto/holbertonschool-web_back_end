#!/usr/bin/env python3
"""
App module
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index() -> str:
    """ Index render route """
    return render_template('0-index.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")
