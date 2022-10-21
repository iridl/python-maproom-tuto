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

import dash_leaflet as dlf # Lesson 2
from dash import dcc # Lesson 4


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
                    dbc.Col(
                        [
                            dbc.Row(
                                dbc.Col(
                                    map_layout(),
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
                }
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        id="variable",
                        clearable=False,
                        options=[
                            dict(label="Precipitation", value="prcp"),
                        ],
                        value="prcp",
                    )
                ],
                style={
                    "display": "inline-block",
                    "vertical-align": "top",
                    "width": "150px",
                }
            ), # Lesson 4 ends
        ],
        sticky="top",
        color="gray",
        dark=True,
    )


def map_layout():
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
                    dlf.ScaleControl(
                        imperial=False,
                        position="bottomleft"),
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
                            Give the data DataArray a colormap attribute such as:
                            """
                        ),
                        html.P(
                            """
                            data.attrs["colormap"] = pingrid.RAINBOW_COLORMAP
                            """
                        ),
                        html.P(
                            """
                            Open layout.py and find the map component.
                            Uncomment the entries that overlays the data layer.
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
                            and move on to Lesson 5.
                            """
                        ),
                    ]),
                ],
            ),
        ],
    )