"""
`maproom.py` defines functions that generate content dynamically
in response to selections made by the user.
It can be run from the command line
to test the application during development.
"""

# Import libraries used
import pingrid
import os
import flask
import dash
import dash_bootstrap_components as dbc

import layout03 as layout

CONFIG = pingrid.load_config(os.environ["CONFIG"])

# Prefix used at the end of the maproom URL
PREFIX = CONFIG["prefix"]

# Defining the server and url
SERVER = flask.Flask(__name__)
APP = dash.Dash(
    __name__,
    server=SERVER,
    url_base_pathname=f"{PREFIX}/",
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        # "https://use.fontawesome.com/releases/v5.12.1/css/all.css",
    ],
)

APP.title = "My First Maproom"
# Calling the app_layout function in `layout.py`
# which includes the layout definitions.
APP.layout = layout.app_layout()

if __name__ == "__main__":
    APP.run_server(
        host=CONFIG["server"],
        port=CONFIG["port"],
        debug=CONFIG["mode"] != "prod"
    )