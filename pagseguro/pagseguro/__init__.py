from flask import Flask
from .trad import configure as trad_config
from .emer import configure as emer_config


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ALSKDJAkljKLJDKLASJDKLjkjKLJkljhklhKLlhJHkjiou8976896785745644636534564564678999'
    trad_config(app)
    emer_config(app)
    return app
