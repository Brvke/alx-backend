#!/usr/bin/env python3
""" first flask app """
from flask import Flask, render_template, request
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


class Config(object):
    """ a class for configaration of babel """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """ return the best match from the Accept-Language header """
    locale = request.args.get('locale')
    if locale in app.config["LANGUAGES"]:
        return locale
    else:
        return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/', strict_slashes=False)
def index():
    """ Prints a Message when / is called """
    return render_template('4-index.html')


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
