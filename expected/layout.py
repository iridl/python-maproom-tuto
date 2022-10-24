"""
The `layout.py` file is used to def a layout function,
which is called within the main maproom.py file
where the maproom is run.

The `layout()` function includes any code which defines the layout of the maproom.
It should not include any callbacks
or directly reference the data be loaded into the maproom.
"""

# Import liBraries used
import dash_bootstrap_components as dbc
from dash import html

import dash_leaflet as dlf # Lesson 2
from dash import dcc # Lesson 4
import xarray as xr # Lesson 6
import numpy as np # Lesson 7
import pingrid # Lesson 10
import os # Lesson 10
from ui_components import Block # Lesson 16


# Lesson 10 starts
CONFIG = pingrid.load_config(os.environ["CONFIG"])
DATA_DIR = CONFIG["data_dir"] # Lesson 10 ends


def app_layout():
    
    # Lesson 6 starts
    data = xr.open_dataarray(
        # "data/CRUprcp.nc", Lesson 10 starts
        DATA_DIR + CONFIG["prcp_file"], # Lesson 10 ends
        decode_times=False
    )
    center_of_the_map = [
        ((data["Y"][int(data["Y"].size/2)].values)),
        ((data["X"][int(data["X"].size/2)].values))
    ] # Lesson 6 ends
    # Lesson 7 starts
    half_res_y = np.abs(data["Y"][1] - data["Y"][0]) / 2
    half_res_x = np.abs(data["X"][1] - data["X"][0]) / 2
    lat_min = (data["Y"][[0, -1]].min() - half_res_y).values
    lat_max = (data["Y"][[0, -1]].max() + half_res_y).values
    lon_min = (data["X"][[0, -1]].min() - half_res_x).values
    lon_max = (data["X"][[0, -1]].max() + half_res_x).values # Lesson 7 ends

    return dbc.Container(
        [
            navbar_layout(),
            dbc.Row(
                [
                    dbc.Col(
                        description_layout(lat_min, lat_max, lon_min, lon_max), # Lesson 16
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
                    dbc.Col(
                        [
                            dbc.Row(
                                dbc.Col(
                                    map_layout(
                                        center_of_the_map,
                                        lon_min,
                                        lat_min,
                                        lon_max,
                                        lat_max), # Lesson 6-7
                                    width=12,
                                    style={
                                        "background-color": "white",
                                    },
                                ),
                            ),
                        ],
                    ),#Lessson 2 ends
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
            html.Div(
                [
                    "Variable:"
                ],
                style={
                    "color": "white",
                    "position": "relative",
                    "display": "inline-block",
                    "vertical-align": "top",
                    "padding": "5px",
                }
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        id="variable",
                        clearable=False,
                        options=[
                            dict(label="Precipitation", value="prcp"),
                            dict(label="Temperature", value="temp"), # Lesson 12
                        ],
                        value="prcp",
                    )
                ],
                style={
                    "display": "inline-block",
                    "vertical-align": "top",
                    "width": "150px",
                    "padding": "5px",
                }
            ), # Lesson 4 ends
            # Lesson 14 starts
            html.Div(
                [
                    "Month:"
                ],
                style={
                    "color": "white",
                    "position": "relative",
                    "display": "inline-block",
                    "vertical-align": "top",
                    "padding": "5px",
                }
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        id="month",
                        clearable=False,
                        options=[
                            dict(label="January", value=1),
                            dict(label="FeBruary", value=2),
                            dict(label="March", value=3),
                            dict(label="April", value=4),
                            dict(label="May", value=5),
                            dict(label="June", value=6),
                            dict(label="July", value=7),
                            dict(label="August", value=8),
                            dict(label="September", value=9),
                            dict(label="October", value=10),
                            dict(label="November", value=11),
                            dict(label="December", value=12),
                        ],
                        value=1,
                    )
                ],
                style={
                    "display": "inline-block",
                    "vertical-align": "top",
                    "width": "130px",
                    "padding": "5px",
                }
            ), # Lesson 14 ends
        ],
        sticky="top",
        color="gray",
        dark=True,
    )


def map_layout(center_of_the_map, lon_min, lat_min, lon_max, lat_max): # Lesson 6-7
    return dbc.Container(
        [
            html.H5(
                id="map_title", # Lesson 15 "A Background Map",
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
                            # Lesson 3 starts
                            dlf.BaseLayer(
                                dlf.TileLayer(
                                    url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"
                                ),
                                name="Street",
                                checked=False,
                            ), # Lesson 3 ends
                            # Lesson 5 starts
                            dlf.Overlay(
                                dlf.TileLayer(
                                    opacity=1,
                                    id="data_layer"
                                ),
                                name="Climate",
                                checked=True,
                            ), # Lesson 5 ends
                        ],
                        position="topleft",
                        id="layers_control",
                    ),
                    # Lesson 16 starts
                    dlf.LayerGroup(
                        [
                            dlf.Marker(
                                id="loc_marker",
                                position=center_of_the_map,
                            )
                        ],
                        id="layers_group",
                    ), # Lesson 16 ends
                    dlf.ScaleControl(
                        imperial=False,
                        position="bottomright"
                    ),
                    # Lesson 8 starts
                    dlf.Colorbar(
                        id="colorbar",
                        min=0,
                        position="bottomleft",
                        width=300,
                        height=10,
                        opacity=.8,
                    ), # Lesson 8 ends
                ],
                id="map",
                center=center_of_the_map, # Lesson 6
                maxBounds=[[lat_min, lon_min],[lat_max, lon_max]], # Lesson 7
                style={
                    "width": "100%",
                    "height": "50vh",
                },
            ),
        ],
        fluid=True,
    )
    
    
def description_layout(lat_min, lat_max, lon_min, lon_max): # Lesson 16
    return dbc.Container(
        [
            html.H5(
                [
                    "This is the Title of this Maproom",
                ]
            ),
            Block("Pick a point",
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.FormFloating(
                                [
                                    dbc.Input(
                                        id="lat_input",
                                        min=lat_min,
                                        max=lat_max,
                                        type="number",
                                    ),
                                    dbc.Label(
                                        "Latitude",
                                        style={"font-size": "80%"},
                                    ),
                                ]
                            ),
                        ),
                        dbc.Col(
                            dbc.FormFloating(
                                [
                                    dbc.Input(
                                        id="lng_input",
                                        min=lon_min,
                                        max=lon_max,
                                        type="number",
                                    ),
                                    dbc.Label(
                                        "Longitude",
                                        style={"font-size": "80%"},
                                    ),
                                ]
                            ),
                        ),
                        dbc.Button(
                            id="submit_lat_lng",
                            n_clicks=0,
                            children='Submit'
                        ),
                    ],
                ),
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
                        html.Code(html.Pre(
                            "https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all"
                        )),
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
                            and move on to Lesson 5.
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
                        html.Code(html.Pre(
                            [
                                'data.attrs["colormap"] = pingrid.RAINBOW_COLORMAP',
                                html.Br(),
                                'data.attrs["scale_min"] = data.min().values',
                                html.Br(),
                                'data.attrs["scale_max"] = data.max().values',
                            ]
                        )),
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
                        html.Code(html.Pre(
                            "tile_pfx: /my_first_maproom/tile"
                        )),
                        html.P(
                            """
                            Open maproom.py and define TILE_PFX
                            along with other prefixes definitions with:
                            """
                        ),
                        html.Code(html.Pre(
                            'TILE_PFX = CONFIG["tile_pfx"]'
                        )),
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
                        html.Code(html.Pre(
                            [
                                'dlf.Colorbar(',
                                html.Br(),
                                '   id="colorbar",',
                                html.Br(),
                                '   position="bottomleft",',
                                html.Br(),
                                '   width=300,',
                                html.Br(),
                                '   height=10,',
                                html.Br(),
                                '   opacity=1,',
                                html.Br(),
                                '),',
                            ]
                        )),
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
                            Add the following Output to the colorscale callback to update attribute tickValues:
                            """
                        ),
                        html.Code(html.Pre(
                            [
                                "[i for i in range(",
                                html.Br(),
                                "   int(data.min().values),",
                                html.Br(),
                                "   int(data.max().values) + 1",
                                html.Br(),
                                ") if i % 10 == 0]",
                            ]
                        )),
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
            html.Details(
                [
                    html.Summary("Lesson 13: Adjust temperature colorscale"),
                    html.Div([
                        html.P(
                            """
                            Study how the ticks of the precipitation colorscale
                            are set up and adapt the temperature one to be more useful
                            """
                        ),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 14.
                            """
                        ),
                    ]),
                ],
            ),
            html.Details(
                [
                    html.Summary("Lesson 14: Map Climatology for a given month"),
                    html.Div([
                        html.P(
                            """
                            Use Xarray to compute the climatology from
                            the monthly data.
                            """
                        ),
                        html.P(
                            """
                            In layout's navbar, make a new dropdown menu
                            that picks values of the dimension of your climatology.
                            """
                        ),
                        html.P(
                            """
                            In maproom, instead of picking the last month of data,
                            pick the month chosen in the layout of the climatological data.
                            Remember to do so for the map and the colorsacle.
                            You will have to pass the dropdown menu momth value
                            in functions and callbacks.
                            Remember also the special case of the map
                            that has a function to create the tiles and
                            another to create the tiles URLs.
                            """
                        ),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 15.
                            """
                        ),
                    ]),
                ],
            ),
            html.Details(
                [
                    html.Summary("Lesson 15: Callback for Map Title"),
                    html.Div([
                        html.P(
                            """
                            We finished our map now. Let's create a callback
                            for the map title to indicate the variable and 
                            month being mapped. The map title is defined
                            at the beginning of the map layout.
                            """
                        ),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 16.
                            """
                        ),
                    ]),
                ],
            ),
            html.Details(
                [
                    html.Summary("Lesson 16: Location Selection"),
                    html.Div([
                        html.P(
                            """
                            We fare going to set up a Marker to pick
                            locations. The Marker will snap to the center
                            of the data gridbox it was clicked in.
                            Additionally, we will put up input text boxes
                            controls to also select longitude and
                            latitude by typing-in. 
                            """
                        ),
                        html.P(
                            """
                            In layout's map component, add a dlf
                            LayersGroup that will contain the Marker. Put
                            it after the LayersControl as:
                            """
                        ),
                        html.Code(html.Pre(
                            [
                                'dlf.LayerGroup(',
                                html.Br(),
                                '   [',
                                html.Br(),
                                '       dlf.Marker(',
                                html.Br(),
                                '           id="loc_marker",',
                                html.Br(),
                                '           position=center_of_the_map,',
                                html.Br(),
                                '       )',
                                html.Br(),
                                '   ],',
                                html.Br(),
                                '   id="layers_group",',
                                html.Br(),
                                '),',
                            ]
                        )),
                        html.P(
                            """
                            Note that we are using center_of_the_map that
                            we used earlier to center the map over our
                            data to give a default position to the Marker.
                            """
                        ),
                        html.P(
                            """
                            In layout's description component, we will
                            add, after out text describing the Maproom
                            the type-in controls as another mean to input
                            latitude and longitude. We will use our UI
                            component Block to make sure they keep tight
                            together in the app. Below is an example
                            adding the latitude control. Add that and
                            include in another Col in the Block a control
                            for longitude.
                            """
                        ),
                        
                        html.P(
                            """
                            Now that we have our Marker and control ready,
                            in maproom, find the callback for
                            pick_location and uncomment it. Note that we
                            need to read data here again to get the data's
                            longitude and latitude. Make sure the data
                            reading is in accordance with the current
                            state of your maproom.
                            """
                        ),
                        html.Code(html.Pre([
                            'Block("Pick a point",',
                            html.Br(),
                            '    dbc.Row(',
                            html.Br(),
                            '        [',
                            html.Br(),
                            '            dbc.Col(',
                            html.Br(),
                            '                dbc.FormFloating(',
                            html.Br(),
                            '                    [',
                            html.Br(),
                            '                        dbc.Input(',
                            html.Br(),
                            '                            id="lat_input",',
                            html.Br(),
                            '                            min=lat_min,',
                            html.Br(),
                            '                            max=lat_max,',
                            html.Br(),
                            '                            type="number",',
                            html.Br(),
                            '                        ),',
                            html.Br(),
                            '                        dbc.Label(',
                            html.Br(),
                            '                            "Latitude",',
                            html.Br(),
                            '                            style={"font-size": "80%"},',
                            html.Br(),
                            '                        ),',
                            html.Br(),
                            '                    ],',
                            html.Br(),
                            '                ),',
                            html.Br(),
                            '            ),',
                            html.Br(),
                            '            dbc.Button(',
                            html.Br(),
                            '                id="submit_lat_lng",',
                            html.Br(),
                            '                n_clicks=0,',
                            html.Br(),
                            '                children="Submit",',
                            html.Br(),
                            '            ),',
                            html.Br(),
                            '        ],',
                            html.Br(),
                            '    ),',
                            html.Br(),
                            '),',
                        ])),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 17.
                            """
                        ),
                    ]),
                ],
            ),
        ],
    )