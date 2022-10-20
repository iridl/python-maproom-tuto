"""
`maproom.py` defines functions that generate content dynamically in response to selections made by the user.
It can be run from the command line to test the application during development.
"""
# Import libraries used
import os
import flask
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import layout

import pingrid

from pathlib import Path
import pyaconf
import pandas as pd
import numpy as np
import xarray as xr
import math

import urllib

from ui_components import Options

import json
from shapely import geometry

import rasterio as rio

CONFIG = pingrid.load_config(os.environ["CONFIG"])

DATA_DIR = CONFIG["data_dir"] # Path to data
PREFIX = CONFIG["prefix"] # Prefix used at the end of the maproom url
TILE_PFX = CONFIG["tile_pfx"] # Prefix used to load the tile layers

# Loading the data
DATA = {}
for d in list(CONFIG["vars"].values()):
    data = xr.open_dataarray(DATA_DIR + "/" + d + ".nc", decode_times=False)
    DATA[d] = data
    DATA[d].attrs["max"] = data.max()
    DATA[d].attrs["min"] = data.min()
    DATA[d].attrs["res"] = DATA[d]['X'][1].item() - DATA[d]['X'][0].item()
# Loading the geometries for the admin layers in the map
SHAP = {}
with open(DATA_DIR + "LSO-ADM0.geojson") as f:
    SHAP["ADM0"] = json.loads(f.read())
with open(DATA_DIR + "LSO-ADM1.geojson") as f:
    SHAP["ADM1"] = json.loads(f.read())
with open(DATA_DIR + "LSO-ADM2.geojson") as f:
    SHAP["ADM2"] = json.loads(f.read())

ADM0 = geometry.Polygon(SHAP["ADM0"]['features'][0]['geometry']['coordinates'][0])

ADM1 = {}
for feat in SHAP["ADM1"]['features']:
    ADM1[feat['properties']['shapeName']] = geometry.Polygon(feat['geometry']['coordinates'][0])

ADM2 = {}
for feat in SHAP["ADM2"]['features']:
    ADM2[feat['properties']['shapeName']] = geometry.Polygon(feat['geometry']['coordinates'][0])

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

APP.title = CONFIG["map_title"]
APP.layout = layout.layout() # Calling the layout function in `layout.py` which includes the layout definitions.

@APP.callback( # Call back definition for `set_region` callback
    Output("region", "options"), # Output of the callback will be the 'options' property of the component with id='region' in the layout.
    Output("region", "value"), # Output of the callback will be the 'value' property of the component with id='region' in the layout.
    Output("region-container", "hidden"), # Output of the callback will be the 'hidden' property of the component with id='region-container' in the layout.
    Output("map_borders", "data"), # Output of the callback will be the 'data' property of the component with id='map-borders' in the layout.
    Input("Spatially Average Over","value"), # Input of the callback which is the 'value' property of the component id='Spatially Average Over'.
)
def set_region(spatial):
    if spatial == "National":
        return [""], "", True, {"features": []}
    elif spatial == "Council":
        opts = sorted(ADM2.keys())
        return Options(opts), opts[0], False, SHAP["ADM2"] #The label and values for `Options()` can be set to not be equal. See documentation in ui_components.py
    elif spatial == "District":
        opts = sorted(ADM1.keys())
        return Options(opts), opts[0], False, SHAP["ADM1"]

@APP.callback( # Callback to create the polygon region layer
    Output("map_selected", "positions"),
    Input("Spatially Average Over","value"),
    Input("region", "value"),
)
def outline_region(spatial, region):
    if spatial == "National":
        return pingrid.poly_shapely_to_leaflet(ADM0)
    elif spatial == "Council":
        return pingrid.poly_shapely_to_leaflet(ADM2[region])
    elif spatial == "District":
        return pingrid.poly_shapely_to_leaflet(ADM1[region])

@APP.callback( # Callback to return the raster layer of the map
    Output("map_raster", "url"),
    Input("Variable", "value"),
    Input("mon0", "value"),
)
def update_map(variable, month):
    var = CONFIG["vars"][variable]

    mon = { "jan": 1, "feb": 2, "mar": 3, "apr": 4,
            "may": 5, "jun": 6, "jul": 7, "aug": 8,
            "sep": 9, "oct": 10, "nov": 11, "dec": 12 }[month]

    qstr = urllib.parse.urlencode({
        "variable": var,
        "month": mon,
    })

    return f"{TILE_PFX}/{{z}}/{{x}}/{{y}}?{qstr}"


def clip_data(data, level, region): # A function not defined as a part of a callback
    res = data.attrs["res"]

    lon_min = data["X"].values[0] - 0.5 * res
    lon_max = data["X"].values[-1] + 0.5 * res
    lat_min = data["Y"].values[0] - 0.5 * res
    lat_max = data["Y"].values[-1] + 0.5 * res

    lon_size = data.sizes["X"]
    lat_size = data.sizes["Y"]

    t = rio.transform.Affine(
        (lon_max - lon_min) / lon_size,
        0,
        lon_min,
        0,
        (lat_max - lat_min) / lat_size,
        lat_min,
    )

    if level == "National":
        geo = ADM0
    elif level == "Council":
        geo = ADM2[region]
    elif level == "District":
        geo = ADM1[region]

    mask = rio.features.geometry_mask([geo], out_shape=(len(data.Y), len(data.X)),
                                      transform=t, all_touched=True, invert=True)
    mask = xr.DataArray(mask, dims=("Y", "X"))
    masked = data.where(mask == True)
    return masked


@SERVER.route(f"/{TILE_PFX}/<int:tz>/<int:tx>/<int:ty>") # Here we connect to the server to access and return the tile layer
def tile(tz, tx, ty):
    parse_arg = pingrid.parse_arg
    var = parse_arg("variable")
    month = parse_arg("month", int)

    x_min = pingrid.tile_left(tx, tz)
    x_max = pingrid.tile_left(tx + 1, tz)
    # row numbers increase as latitude decreases
    y_max = pingrid.tile_top_mercator(ty, tz)
    y_min = pingrid.tile_top_mercator(ty + 1, tz)
    data = DATA[var]
    resolution = data.attrs["res"]

    if (
            x_min > data['X'].max() or
            x_max < data['X'].min() or
            y_min > data['Y'].max() or
            y_max < data['Y'].min()
    ):
        return pingrid.empty_tile()

    tile = data.sel(
        X=slice(x_min - x_min % resolution, x_max + resolution - x_max % resolution),
        Y=slice(y_min - y_min % resolution, y_max + resolution - y_max % resolution),
        T=month - 0.5
    ).compute()

    tile.attrs["colormap"] = pingrid.RAINBOW_COLORMAP
    tile = tile.rename(X="lon", Y="lat")
    if var == "diff":
        tile.attrs["scale_min"] = np.float64(data.attrs["min"])
    else:
        tile.attrs["scale_min"] = np.float64(0)
    tile.attrs["scale_max"] = np.float64(data.attrs["max"])

    result = pingrid.tile(tile, tx, ty, tz, ADM0)

    return result

@SERVER.route(f"{PREFIX}/health")
def health_endpoint():
    return flask.jsonify({'status': 'healthy', 'name': 'python_maproom'})


if __name__ == "__main__":
    APP.run_server(
        host=CONFIG["server"],
        port=CONFIG["port"],
        debug=CONFIG["mode"] != "prod"
    )
