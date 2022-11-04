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
import plotly.express as px # Lesson 17


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
    Input("month", "value"), # Lesson 14
)
def data_tile_url_callback(variable, month): # Lesson 14
    return f"{TILE_PFX}/{{z}}/{{x}}/{{y}}/{variable}/{month}" # Lesson 5 ends, 14


# Lesson 5 starts
@SERVER.route(
    f"{TILE_PFX}/<int:tz>/<int:tx>/<int:ty>/<variable>/<this_month>" # Lesson 14
)
def data_tiles(tz, tx, ty, variable, this_month): # Lesson 14
    if variable == "pre":
        data_file = CONFIG["prcp_file"]
    else:
        data_file = CONFIG["temp_file"] # Lesson 12 ends
    data = xr.open_dataset(
        # "data/CRUprcp.nc", Lesson 10 starts
        #DATA_DIR + CONFIG["prcp_file"], # Lesson 10 ends
        DATA_DIR + data_file, # Lesson 12
        decode_times=False
    )
    data["T"].attrs["calendar"] = "360_day"
    data = xr.decode_cf(data, decode_times=True).rename(
        {"X": "lon", "Y": "lat"}
    )[variable] # .isel(T=-1) # Lesson 5, 14
    data = data.groupby("T.month").mean()
    map_min = data.min().values
    map_max = data.max().values
    data = data.sel(month=int(this_month))
    data.attrs["colormap"] = pingrid.RAINBOW_COLORMAP # Lesson 5 
    data.attrs["scale_min"] = map_min
    data.attrs["scale_max"] = map_max
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
def set_colorbar(variable): # Lesson 14
    # Lesson 12 starts
    if variable == "pre":
        data_file = CONFIG["prcp_file"]
        ticks_sample = 10 # Lesson 13
    else:
        data_file = CONFIG["temp_file"] # Lesson 12 ends
        ticks_sample = 1 # Lesson 13
    data = xr.open_dataset(
        # "data/CRUprcp.nc", Lesson 10 starts
        #DATA_DIR + CONFIG["prcp_file"], # Lesson 10 ends
        DATA_DIR + data_file, # Lesson 12
        decode_times=False
    )
    data["T"].attrs["calendar"] = "360_day"
    data = xr.decode_cf(data, decode_times=True).rename(
        {"X": "lon", "Y": "lat"}
    )[variable] # .isel(T=-1) # Lesson 5, 14
    data = data.groupby("T.month").mean()
    map_min = data.min().values
    map_max = data.max().values
    return (
        pingrid.to_dash_colorscale(pingrid.RAINBOW_COLORMAP),
        map_min,
        map_max,
        # Lesson 9 starts
        [i for i in range(
            int(map_min),
            int(map_max) + 1
        ) if i % ticks_sample == 0] # Lesson 9 ends, 13
    ) # Lesson 8 ends


# Lesson 15 starts
@APP.callback(
    Output("map_title", "children"),\
    Input("variable", "value"),
    Input("month", "value"),
)
def write_map_title(variable, month):
    if variable == "pre":
        variable = "Precipitation"
    else:
        variable = "Temperature"
    month_label = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "september",
        10: "October",
        11: "November",
        12: "December",
    }
    return f'{variable} Climatology in {month_label[month]}' # Lesson 15 ends


# Lesson 16 starts
@APP.callback(
    Output("loc_marker", "position"),
    Output("lat_input", "value"),
    Output("lng_input", "value"),
    Input("submit_lat_lng","n_clicks"),
    Input("map", "click_lat_lng"),
    State("lat_input", "value"),
    State("lng_input", "value")
)
def pick_location(n_clicks, click_lat_lng, latitude, longitude):
    # Reading
    data = xr.open_dataarray(
        DATA_DIR + CONFIG["prcp_file"],
        decode_times=False,
    )
    if dash.ctx.triggered_id == None:
        lat = data["Y"][int(data["Y"].size/2)].values
        lng = data["X"][int(data["X"].size/2)].values
    else:
        if dash.ctx.triggered_id == "map":
            lat = click_lat_lng[0]
            lng = click_lat_lng[1]
        else:
            lat = latitude
            lng = longitude
        try:
            nearest_grid = pingrid.sel_snap(data, lat, lng)
            lat = nearest_grid["Y"].values
            lng = nearest_grid["X"].values
        except KeyError:
            lat = lat
            lng = lng
    return [lat, lng], lat, lng # Lesson 16 ends


# Lesson 17 starts
@APP.callback(
    Output("clim_plot", "figure"),
    Input("loc_marker", "position"),
    Input("variable", "value")
)
def create_plot(marker_loc, variable):
    lat = marker_loc[0]
    lng = marker_loc[1]
    if variable == "pre":
        data_file = CONFIG["prcp_file"]
        variable = "Precipition"
    else:
        data_file = CONFIG["temp_file"]
        variable = "Temperature"
    data = xr.open_dataarray(
        DATA_DIR + data_file,
        decode_times=False,
    )
    data = data.groupby(data["T"] % 12 + 0.5).mean()
    data = pingrid.sel_snap(data, lat, lng)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    bar_plot = px.bar(
        data, x=months, y=data,
        title = f"{variable} monthly climatology",
        labels = {
            "x": "Time (months)",
            "y": f"{variable} ({data.attrs['units']})",
        },
    )
    return bar_plot # Lesson 17 ends


if __name__ == "__main__":
    APP.run_server(
        host=CONFIG["server"],
        port=CONFIG["port"],
        debug=CONFIG["mode"] != "prod"
    )