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


# def get_locale():
#     """ Get the local from the Config class """
#     return request.accept_languages.best_match(Config.LANGUAGES)


app = Flask(__name__)
babel = Babel(
    app,
    default_locale=Config.LANGUAGES[0],
    default_timezone=Config.TZ.zone
)


@app.route("/", methods=["GET"])
def index() -> str:
    """ Index render route """
    return render_template('1-index.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")
