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
                    "This is the Title of this Maproom",
                ]
            ),
            html.Details(
                [
                    html.Summary("Lesson 1: Titles and text"),
                    html.Div([
                        html.P(
                            """
                            Open layout01.py and identify where are the text for:
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
                    html.Summary("Lesson 2: TBD"),
                    html.Div(
                        html.P(
                            """
                            tbd
                            """
                        ),
                    )
                ],
            ),
        ],
    )