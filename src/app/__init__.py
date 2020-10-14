# -*- coding: utf-8 -*-
"""Main application factory."""
import flask
from .dashboard import register_dashboard


def create_app():
    """Flask backend serving plotly dashboard."""
    app = flask.Flask(__name__)
    register_dashboard(app)

    return app
