#!/usr/bin/env python3
""" first flask app """
from flask import Flask, render_template, request, g
from flask_babel import Babel
from pytz import timezone

app = Flask(__name__)
babel = Babel(app)

class Config(object):
    """ a class for configaration of babel """
    LANGUAGES =  ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)

@babel.localeselector
def get_locale():
    """ return the best match from the Accept-Language header """
    locale = request.args.get('locale')
    if locale in app.config["LANGUAGES"]:
        return locale
    elif g.user is not None and g.user["locale"] in app.config["LANGUAGES"]:
        return g.user["locale"]
    elif request.headers.get('Accept-Language') is not None:
        return request.headers.get('Accept-Language')[:2]
    else:
        return app.config['BABEL_DEFAULT_LOCALE']

@babel.timezoneselector
def get_timezone():
    """ return the best matching timezones """
    time = request.args.get('timezone')
    if time is None:
        time = request.args.get('Time-Zone')
    elif g.user:
        g.user.get('timezone')
    
    try:
        return timezone(time).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


def get_user():
    """ gets user from dict """

    users = {
        1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
        2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
        3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
        4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
    }

    user_id = request.args.get('login_as')
    if user_id is not None:
        user_id = int(user_id)
    if user_id in users.keys():
        return users[user_id]
    else:
        return None

@app.before_request
def before_request():
    """ function to be used before all others """
    g.user = get_user()

@app.route('/', strict_slashes=False)
def index():
    """ Prints a Message when / is called """
    return render_template('7-index.html')

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)