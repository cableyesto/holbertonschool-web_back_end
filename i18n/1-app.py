#!/usr/bin/env python3
"""
App module
"""
from flask import Flask, request, render_template
from flask_babel import Babel
from pytz import timezone


class Config:
    """ Configuration class of the flask app """
    LANGUAGES = ["en", "fr"]
    TZ = timezone("UTC")
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route("/", methods=["GET"])
def index() -> str:
    """ Index render route """
    return render_template('1-index.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")
