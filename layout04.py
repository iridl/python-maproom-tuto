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
import dash_leaflet as dlf
from dash import dcc


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
                    ),
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
                                "Monthly Climatology",
                                className="ml-2",
                            )
                        ),
                    ],
                    align="center", style={"padding-left":"5px"}
                ),
            ),
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
            #            options=[
            #                dict(label="Precipitation", value="prcp"),
            #            ],
            #            value="prcp",
            #        )
            #    ],
            #    style={
            #        "display": "inline-block",
            #        "vertical-align": "top",
            #    }
            #),
        ],
        sticky="top",
        color="gray",
        dark=True,
    )
    
    
def description_layout():
    return dbc.Container(
        [
            html.H5(
                [
                    "Monthly Climatology",
                ]
            ),
            html.P(
                """
                This Maprooms explore monthly climatologies.
                """
            ),
            html.P(
                [
                    """
                    Instructions:
                    """
                ],
                style={"color": "red"}
            ),
            html.P(
                """
                Open layout04.py and find the navigation bar component.
                Uncomment the new entries that set up a Variable menu.
                """
            ),
            html.P(
                """
                When you are done, run maproom05.py for the next exercise
                """
            ),
        ],
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
                            dlf.BaseLayer(
                                dlf.TileLayer(
                                    url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"
                                ),
                                name="Street",
                                checked=False,
                            ),
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