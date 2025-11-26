#!/usr/bin/env python3
"""
App module
"""
import flask
from flask import Flask, request, render_template, g
from flask_babel import Babel
import pytz
from pytz import timezone


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """ Configuration class of the flask app """
    LANGUAGES = ["en", "fr"]
    TZ = timezone("UTC")
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


def get_locale():
    """ Obtain the locale of the user """
    locale = request.args.get('locale')
    is_valid_locale = locale in app.config['LANGUAGES']
    if locale and is_valid_locale:
        return locale

    user_id = request.args.get('login_as')
    if user_id:
        user_id = int(user_id)
        user = get_user(user_id)
        user_locale = user.get('locale')
        if user_locale in app.config['LANGUAGES']:
            return user_locale

    if request.accept_languages:
        return Config.BABEL_DEFAULT_LOCALE

    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user(user_id):
    """Get user."""
    return users.get(user_id)


# @babel.timezoneselector
def get_timezone():
    """Obtain the timezone of the user."""
    # Third option executed first because variable will be reallocated
    final_tz_default = Config.BABEL_DEFAULT_TIMEZONE
    final_tz_str = ''

    # Second option
    user_id = request.args.get('login_as')
    if user_id:
        user_id = int(user_id)
        user = get_user(user_id)
        user_tz = user.get('timezone')
        final_tz_str = user_tz

    # First option
    timezone = request.args.get('timezone')
    if timezone:
        final_tz_str = timezone

    try:
        return timezone(final_tz_str)
    except pytz.exceptions.UnknownTimeZoneError:
        return timezone(final_tz_default)


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)
babel.init_app(app, locale_selector=get_locale, timezone_selector=get_timezone)


@app.before_request
def before_request():
    """Obtain the user before every request."""
    user_id = request.args.get('login_as')
    user_id = int(user_id) if user_id else None
    user = get_user(user_id)
    flask.g.user = user


@app.context_processor
def inject_user():
    """Inject user in template."""
    return {'current_user': g.get('user')}


@app.route("/", methods=["GET"])
def index() -> str:
    """ Index render route """
    return render_template('6-index.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")
