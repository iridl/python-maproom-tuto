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

#from dash.dependencies import Output, Input, State # Lesson 5
#import xarray as xr # Lesson 5
#import numpy as np # Lesson 9


CONFIG = pingrid.load_config(os.environ["CONFIG"])

# Prefixes used by URLs
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


# Lesson 5 starts
#@APP.callback(
#    Output("data_layer", "url"),
#    Input("variable", "value"),
#)
#def data_tile_url_callback(variable):
#    return f"{TILE_PFX}/{{z}}/{{x}}/{{y}}/{variable}" # Lesson 5 ends


# Lesson 5 starts
#@SERVER.route(
#    f"{TILE_PFX}/<int:tz>/<int:tx>/<int:ty>/<variable>"
#)
#def data_tiles(tz, tx, ty, variable):
#    data = 0
#    resp = pingrid.tile(data, tx, ty, tz)
#    return resp # Lesson 5 ends


# Lesson 8 starts
#@APP.callback(
#    Output("colorbar", "colorscale"),
#    Output("colorbar", "min"),
#    Output("colorbar", "max"),
#    Input("variable", "value"),
#)
#def set_colorbar(variable):
#    data = 0
#    return (
#        pingrid.to_dash_colorscale(pingrid.RAINBOW_COLORMAP),
#        data.min().values,
#        data.max().values,
#    ) # Lesson 8 ends


# Lesson 16 starts
#@APP.callback(
#    Output("loc_marker", "position"),
#    Output("lat_input", "value"),
#    Output("lng_input", "value"),
#    Input("submit_lat_lng","n_clicks"),
#    Input("map", "click_lat_lng"),
#    State("lat_input", "value"),
#    State("lng_input", "value")
#)
#def pick_location(n_clicks, click_lat_lng, latitude, longitude):
#    # Reading
#    data = xr.open_dataarray(
#        DATA_DIR + CONFIG["prcp_file"],
#        decode_times=False,
#    )
#    if dash.ctx.triggered_id == None:
#        lat = data["Y"][int(data["Y"].size/2)].values
#        lng = data["X"][int(data["X"].size/2)].values
#    else:
#        if dash.ctx.triggered_id == "map":
#            lat = click_lat_lng[0]
#            lng = click_lat_lng[1]
#        else:
#            lat = latitude
#            lng = longitude
#        try:
#            nearest_grid = pingrid.sel_snap(data, lat, lng)
#            lat = nearest_grid["Y"].values
#            lng = nearest_grid["X"].values
#        except KeyError:
#            lat = lat
#            lng = lng
#    return [lat, lng], lat, lng # Lesson 16 ends
            

if __name__ == "__main__":
    APP.run_server(
        host=CONFIG["server"],
        port=CONFIG["port"],
        debug=CONFIG["mode"] != "prod"
    )