"""
The `layout.py` file is used to def a layout function,
which is called within the main maproom.py file
where the maproom is run.

The `layout()` function includes any code which defines the layout of the maproom.
It should not include any callbacks
or directly reference the data be loaded into the maproom.
"""

# Import libraries used
import dash_bootstrap_components as dbc
from dash import html

#import dash_leaflet as dlf # Lesson 2
#from dash import dcc # Lesson 4
#import xarray as xr # Lesson 6
#import numpy as np # Lesson 7
#import pingrid # Lesson 10
#import os # Lesson 10


def app_layout():

    return dbc.Container(
        [
            navbar_layout(),
            dbc.Row(
                [
                    dbc.Col(
                        description_layout(),
                        sm=12,
                        md=4,
                        style={
                            "background-color": "white",
                            "border-style": "solid",
                            "border-color": "lightGray",
                            "border-width": "0px 1px 0px 0px",
                        },
                    ),
                    #Lesson 2 starts
                    #dbc.Col(
                    #    [
                    #        dbc.Row(
                    #            dbc.Col(
                    #                map_layout(), # Lesson 6-7
                    #                width=12,
                    #                style={
                    #                    "background-color": "white",
                    #                },
                    #            ),
                    #        ),
                    #    ],
                    #),#Lessson 2 ends
                ],
            ),
        ],
        fluid=True,
        style={"padding-left": "0px", "padding-right": "0px"},
    )

    
def navbar_layout():
    return dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.NavbarBrand(
                                "This is the Navigation bar where we will put controls and website navigation",
                                className="ml-2",
                            )
                        ),
                    ],
                    align="center", style={"padding-left":"5px"}
                ),
            ),
            # Lesson 4 starts
            #html.Div(
            #    [
            #        "Variable:"
            #    ],
            #    style={
            #        "color": "white",
            #        "position": "relative",
            #        "display": "inline-block",
            #        "vertical-align": "top",
            #    }
            #),
            #html.Div(
            #    [
            #        dcc.Dropdown(
            #            id="variable",
            #            clearable=False,
            #            options=[
            #                dict(label="Precipitation", value="prcp"),
            #            ],
            #            value="prcp",
            #        )
            #    ],
            #    style={
            #        "display": "inline-block",
            #        "vertical-align": "top",
            #        "width": "150px",
            #    }
            #), # Lesson 4 ends
        ],
        sticky="top",
        color="gray",
        dark=True,
    )


def map_layout(): # Lesson 6-7
    return dbc.Container(
        [
            html.H5(
                "A Background Map",
                style={
                    "text-align":"center",
                    "border-width":"1px",
                    "border-style":"solid",
                    "border-color":"grey",
                    "margin-top":"3px",
                    "margin-bottom":"3px"},
            ),
            dlf.Map(
                [
                    dlf.LayersControl(
                        [
                            dlf.BaseLayer(
                                dlf.TileLayer(
                                    url="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
                                ),
                                name="Topo",
                                checked=True,
                            ),
                            # Lesson 5 starts
                            #dlf.Overlay(
                            #    dlf.TileLayer(
                            #        opacity=1,
                            #        id="data_layer"
                            #    ),
                            #    name="Climate",
                            #    checked=True,
                            #), # Lesson 5 ends
                        ],
                        position="topleft",
                        id="layers_control",
                    ),
                    dlf.ScaleControl(
                        imperial=False,
                        position="bottomright"
                    ),
                ],
                id="map",
                style={
                    "width": "100%",
                    "height": "50vh",
                },
            ),
        ],
        fluid=True,
    )
    
    
def description_layout():
    return dbc.Container(
        [
            html.H5(
                [
                    "This is the Title of this Maproom",
                ]
            ),
            html.Details(
                [
                    html.Summary("Lesson 1: Titles and text"),
                    html.Div([
                        html.P(
                            """
                            Open layout.py and identify where are the text for:
                            the Navigation bar (navbar_layout);
                            for the Title (description_layout);
                            and change them.
                            """
                        ),
                        html.P(
                            """
                            Add another paragraph describing this Maproom between its Title and these Instructions.
                            """
                        ),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 2.
                            """
                        ),
                    ]),
                ],
            ),
            html.Details(
                [
                    html.Summary("Lesson 2: Topo background map"),
                    html.Div([
                        html.P(
                            """
                            Open layout.py and find the commented Col component
                            containing the map_layout.
                            Uncomment it to make appear a background topographic map
                            in the right pannel.
                            """
                        ),
                        html.P(
                            """
                            Have a look at map_layout()
                            """
                        ),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 3.
                            """
                        ),
                    ]),
                ],
            ),
            html.Details(
                [
                    html.Summary("Lesson 3: Add Street background map"),
                    html.Div([
                        html.P(
                            """
                            Open layout.py and find where the Topo layer is defined.
                            Add the following Street layer as another option
                            for background mapping.
                            """
                        ),
                        html.P(
                            """
                            https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all
                            """
                        ),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 4.
                            """
                        ),
                    ]),
                ],
            ),
            html.Details(
                [
                    html.Summary("Lesson 4: Set a Variable Dropdown menu"),
                    html.Div([
                        html.P(
                            """
                            Open layout.py and find the navigation bar component.
                            Uncomment the new entries that set up a Variable menu.
                            """
                        ),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 4.
                            """
                        ),
                    ]),
                ],
            ),
            html.Details(
                [
                    html.Summary("Lesson 5: Add a data layer to the map"),
                    html.Div([
                        html.P(
                            """
                            Read data file data/CRUprcp.nc as a DataArray
                            renaming its X/Y dimensions to lon/lat
                            and selecting the last time point
                            """
                        ),
                        html.P(
                            """
                            In maproom.py, find the data_tiles function.
                            Uncomment it and replace the data with your calculation.
                            """
                        ),
                        html.P(
                            """
                            Give the data DataArray a colormap attribute,
                            as well as scale_min and scale_max attributes, such as:
                            """
                        ),
                        html.P(
                            """
                            data.attrs["colormap"] = pingrid.RAINBOW_COLORMAP
                            """
                        ),
                        html.P(
                            """
                            data.attrs["scale_min"] = data.min().values
                            """
                        ),
                        html.P(
                            """
                            data.attrs["scale_max"] = data.max().values
                            """
                        ),
                        html.P(
                            """
                            Open layout.py and find the Map component.
                            Uncomment the entries that overlay the data layer.
                            """
                        ),
                        html.P(
                            """
                            Open maproom.py and find the callback creating data tiles URL
                            and uncomment it.
                            """
                        ),
                        html.P(
                            """
                            Open config-sample.yaml and define the tiles prefix with:
                            """
                        ),
                        html.P(
                            """
                            tile_pfx: /my_first_maproom/tile
                            """
                        ),
                        html.P(
                            """
                            Open maproom.py and define TILE_PFX
                            along with other prefixes definitions with:
                            """
                        ),
                        html.P(
                            """
                            TILE_PFX = CONFIG["tile_pfx"]
                            """
                        ),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 6.
                            """
                        ),
                    ]),
                ],
            ),
            html.Details(
                [
                    html.Summary("Lesson 6: Automatically center map on data"),
                    html.Div([
                        html.P(
                            """
                            Create a [lat, lon] array assigned to center_of_the_map
                            where lat and lon are the coordinates of the center of data
                            and define center_of_the_map at the beginning of app_layout
                            """
                        ),
                        html.P(
                            """
                            In layout.py, have center_of_the_map be an argument of map_layout.
                            Then give the dlf Map component center_of_the_map as center attribute.
                            """
                        ),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 7.
                            """
                        ),
                    ]),
                ],
            ),
            html.Details(
                [
                    html.Summary("Lesson 7: Prevent dragging far from data"),
                    html.Div([
                        html.P(
                            """
                            Compute the longitude and latitude values
                            of the edges of the domain and assign them to variables
                            along with center_of_the_map
                            """
                        ),
                        html.P(
                            """
                            Pass those 4 values to map_layout,
                            and give the dlf Map component
                            [[lat_min, lon_min],[lat_max, lon_max]]
                            as maxBounds attribute.
                            """
                        ),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 8.
                            """
                        ),
                    ]),
                ],
            ),
            html.Details(
                [
                    html.Summary("Lesson 8: Add the colorscale"),
                    html.Div([
                        html.P(
                            """
                            Add a dlf Colorbar component to the dlf Map with:
                            """
                        ),
                        html.P(
                            """
                            dlf.Colorbar(
                                id="colorbar",
                                position="bottomleft",
                                width=300,
                                height=10,
                                opacity=1,
                            ),
                            """
                        ),
                        html.P(
                            """
                            In maproom.py, find the set_colorbar callback.
                            Uncomment it and make sure it is using the same
                            colorscale, min and max values as the data ones.
                            """
                        ),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 9.
                            """
                        ),
                    ]),
                ],
            ),
            html.Details(
                [
                    html.Summary("Lesson 9: Tick colorscale every 10"),
                    html.Div([
                        html.P(
                            """
                            Add the following Output to the colorscale callback:
                            """
                        ),
                        html.P(
                            """
                            [i for i in range(
                                int(data.min().values),
                                int(data.max().values) + 1
                            ) if i % 10 == 0]
                            """
                        ),
                        html.P(
                            """
                            Output("colorbar", "tickValues")
                            """
                        ),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 10.
                            """
                        ),
                    ]),
                ],
            ),
            html.Details(
                [
                    html.Summary("Lesson 10: Configure data source"),
                    html.Div([
                        html.P(
                            """
                            In the config file, add a new entry for the path
                            of the directorty where the data file is,
                            and another entry for the filename.
                            """
                        ),
                        html.P(
                            """
                            Replace all instances of data file reading in
                            maproom.py and layout.py with the strings from config.
                            """
                        ),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 11.
                            """
                        ),
                    ]),
                ],
            ),
            html.Details(
                [
                    html.Summary("Lesson 11: Use other data"),
                    html.Div([
                        html.P(
                            """
                            The Maproom should work with any nc file
                            with X, Y and T dimensions. If you have access to some,
                            get new data for your country of interest.
                            To make best use of the rest of the Tutorial,
                            get 10 years of monthly data. Once you have such a file,
                            overwrite your configuration with the new data sources.
                            Don't commit data files to git. git is a code version
                            control tool, not a place to store data.
                            The NY CRU data is a small sample to allow the Tutorial
                            to stand alone. Store your data files somewhere readable.
                            """
                        ),
                        html.P(
                            """
                            When you are done, move on to Lesson 12.
                            """
                        ),
                    ]),
                ],
            ),
            html.Details(
                [
                    html.Summary("Lesson 12: Add another variable: temperature"),
                    html.Div([
                        html.P(
                            """
                            Get temperature data from the same source you just
                            got new precipitation data (or continue to work with
                            the NY CRU data). Save the data file in same place 
                            as precipitation one and indicate the name of the 
                            temperature file in the config.
                            """
                        ),
                        html.P(
                            """
                            In the layout, go back to the dropdown menu we set up
                            for precipitation and add a temperature option.
                            """
                        ),
                        html.P(
                            """
                            In maproom.py, use if/else commands to use the right
                            data file based on the value of the dropdown choice.
                            Note that we are also reading the precipitation file
                            in the layout, but that is just to get lon and lat
                            information. Here we assume both variables will come
                            from the same set and thus have same lat/lon. So we
                            are not changing the data reading in the layout.
                            """
                        ),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 13.
                            """
                        ),
                    ]),
                ],
            ),
        ],
    )