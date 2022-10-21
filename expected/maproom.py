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

import layout

from dash.dependencies import Output, Input, State # Lesson 5
import xarray as xr # Lesson 5
import numpy as np # Lesson 9


CONFIG = pingrid.load_config(os.environ["CONFIG"])

# Prefixes used by URLs
PREFIX = CONFIG["prefix"]
TILE_PFX = CONFIG["tile_pfx"] # Lesson 5
DATA_DIR = CONFIG["data_dir"] # Lesson 10

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


# Lesson 5 starts
@APP.callback(
    Output("data_layer", "url"),
    Input("variable", "value"),
)
def data_tile_url_callback(variable):
    return f"{TILE_PFX}/{{z}}/{{x}}/{{y}}/{variable}" # Lesson 5 ends


# Lesson 5 starts
@SERVER.route(
    f"{TILE_PFX}/<int:tz>/<int:tx>/<int:ty>/<variable>"
)
def data_tiles(tz, tx, ty, variable):
    # Lesson 12 starts
    if variable == "prcp":
        data_file = CONFIG["prcp_file"]
    else:
        data_file = CONFIG["temp_file"] # Lesson 12 ends
    data = xr.open_dataarray(
        # "data/CRUprcp.nc", Lesson 10 starts
        #DATA_DIR + CONFIG["prcp_file"], # Lesson 10 ends
        DATA_DIR + data_file, # Lesson 12
        decode_times=False
    ).rename({"X": "lon", "Y": "lat"}).isel(T=-1) # Lesson 5
    data.attrs["colormap"] = pingrid.RAINBOW_COLORMAP # Lesson 5 
    data.attrs["scale_min"] = data.min().values
    data.attrs["scale_max"] = data.max().values
    resp = pingrid.tile(data, tx, ty, tz)
    return resp # Lesson 5 ends


# Lesson 8 starts
@APP.callback(
    Output("colorbar", "colorscale"),
    Output("colorbar", "min"),
    Output("colorbar", "max"),
    Output("colorbar", "tickValues"), # Lesson 9
    Input("variable", "value"),
)
def set_colorbar(variable):
    # Lesson 12 starts
    if variable == "prcp":
        data_file = CONFIG["prcp_file"]
    else:
        data_file = CONFIG["temp_file"] # Lesson 12 ends
    data = xr.open_dataarray(
        # "data/CRUprcp.nc", Lesson 10 starts
        #DATA_DIR + CONFIG["prcp_file"], # Lesson 10 ends
        DATA_DIR + data_file, # Lesson 12
        decode_times=False
    ).isel(T=-1)
    return (
        pingrid.to_dash_colorscale(pingrid.RAINBOW_COLORMAP),
        data.min().values,
        data.max().values,
        # Lesson 9 starts
        [i for i in range(
            int(data.min().values),
            int(data.max().values) + 1
        ) if i % 10 == 0] # Lesson 9 ends
    ) # Lesson 8 ends
        

if __name__ == "__main__":
    APP.run_server(
        host=CONFIG["server"],
        port=CONFIG["port"],
        debug=CONFIG["mode"] != "prod"
    )