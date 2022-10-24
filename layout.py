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
#from ui_components import Block # Lesson 16


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
                            Open layout.py and identify where are the
                            text for: the Navigation bar (navbar_layout);
                            for the Title (description_layout); and
                            change them.
                            """
                        ),
                        html.P(
                            """
                            Add another paragraph describing this Maproom
                            between its Title and these Instructions.
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
                            In layout, we already created map_layout
                            function that creates a topographical map that
                            we mean to use as background for our mapping
                            purposes. Add this map to the app by adding
                            the following Col component in parallel to the
                            Col containing the description layout.
                            """
                        ),
                        html.Code(html.Pre([
                            'dbc.Col(',
                            html.Br(),
                            '    [',
                            html.Br(),
                            '        dbc.Row(',
                            html.Br(),
                            '            dbc.Col(',
                            html.Br(),
                            '                map_layout(),',
                            html.Br(),
                            '                width=12,',
                            html.Br(),
                            '                style={',
                            html.Br(),
                            '                    "background-color": "white",',
                            html.Br(),
                            '                },',
                            html.Br(),
                            '            ),',
                            html.Br(),
                            '        ),',
                            html.Br(),
                            '    ],',
                            html.Br(),
                            '),',
                        ])),
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
                            Open layout.py and find where the Topo layer
                            is defined. Add the following Street layer as
                            another option for background mapping.
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
                            Open layout.py and find the navigation bar
                            component. Add the following 2 new Div
                            components that will put up a dropdown menu to
                            choose variables (currently just one).
                            """
                        ),
                        html.Code(html.Pre([
                            'html.Div(',
                            html.Br(),
                            '    [',
                            html.Br(),
                            '        "Variable:"',
                            html.Br(),
                            '    ],',
                            html.Br(),
                            '    style={',
                            html.Br(),
                            '        "color": "white",',
                            html.Br(),
                            '        "position": "relative",',
                            html.Br(),
                            '        "display": "inline-block",',
                            html.Br(),
                            '        "vertical-align": "top",',
                            html.Br(),
                            '        "padding": "5px",',
                            html.Br(),
                            '    },',
                            html.Br(),
                            '),',
                            html.Br(),
                            'html.Div(',
                            html.Br(),
                            '    [',
                            html.Br(),
                            '        dcc.Dropdown(',
                            html.Br(),
                            '            id="variable",',
                            html.Br(),
                            '            clearable=False,',
                            html.Br(),
                            '            options=[',
                            html.Br(),
                            '                dict(label="Precipitation", value="prcp"),',
                            html.Br(),
                            '            ],',
                            html.Br(),
                            '            value="prcp",',
                            html.Br(),
                            '        )',
                            html.Br(),
                            '    ],',
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            '    style={',
                            html.Br(),
                            html.Br(),
                            '        "display": "inline-block",',
                            html.Br(),
                            '        "vertical-align": "top",',
                            html.Br(),
                            '        "width": "150px",',
                            html.Br(),
                            '        "padding": "5px",',
                            html.Br(),
                            '    },',
                            html.Br(),
                            '),',
                        ])),
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
                            (using Xarray's open_dataarrya) renamining
                            (using Xarray's rename) its X/Y dimensions to
                            lon/lat and selecting (using Xarray's sel)
                            the last time point.
                            """
                        ),
                        html.P(
                            """
                            In maproom.py, we are going to create our
                            first callback that uses our features to make
                            maps. Starts with:
                            """
                        ),
                        html.Code(html.Pre([
                            '@APP.callback(',
                            html.Br(),
                            '    Output("data_layer", "url"),',
                            html.Br(),
                            '    Input("variable", "value"),',
                            html.Br(),
                            ')',
                            html.Br(),
                            'def data_tile_url_callback(variable):',
                            html.Br(),
                            '    return f"{TILE_PFX}/{{z}}/{{x}}/{{y}}/{variable}"',
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            '@SERVER.route(',
                            html.Br(),
                            '    f"{TILE_PFX}/<int:tz>/<int:tx>/<int:ty>/<variable>"',
                            html.Br(),
                            ')',
                            html.Br(),
                            'def data_tiles(tz, tx, ty, variable):',
                        ])),
                        html.P(
                            """
                            Then here include your code to read the data
                            and call that variable data. Give that data
                            DataArray a colormap attribute, as well as
                            scale_min and scale_max attributes, such as:
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
                            And continue with function making tiles as:
                            """
                        ),
                        html.Code(html.Pre([
                            '    resp = pingrid.tile(data, tx, ty, tz)',
                            html.Br(),
                            '    return resp # Lesson 5 ends',
                        ])),
                        html.P(
                            """
                            Open layout.py and find the Map component.
                            Add a new layer to the map's BaseLayers with
                            the tiled data layer we just created.
                            """
                        ),
                        html.Code(html.Pre([
                            'dlf.Overlay(',
                            html.Br(),
                            '    dlf.TileLayer(',
                            html.Br(),
                            '        opacity=1,',
                            html.Br(),
                            '        id="data_layer"',
                            html.Br(),
                            '    ),',
                            html.Br(),
                            '    name="Climate",',
                            html.Br(),
                            '    checked=True,',
                            html.Br(),
                            '),',
                        ])),
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
                            Create a [lat, lon] array assigned to
                            center_of_the_map where lat and lon are the
                            coordinates of the center of data and define
                            center_of_the_map at the beginning of
                            app_layout
                            """
                        ),
                        html.P(
                            """
                            In layout.py, have center_of_the_map be an argument of map_layout. Then give the dlf
                            Map component center_of_the_map as center attribute.
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
                            Compute the longitude and latitude values of
                            the edges of the domain and assign them to
                            variables along with center_of_the_map.
                            """
                        ),
                        html.P(
                            """
                            Pass those 4 values to map_layout, and give
                            the dlf Map component
                            [[lat_min, lon_min], [lat_max, lon_max]]
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
                            Add a dlf Colorbar component to the dlf Map
                            with:
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
                            We now need a new callback to set the
                            colorscale and a few other of its attributes.
                            In maproom.py, create a callback that outputs the colorbar's colorscale, min and
                            max and that take variable as Input. Then
                            create the callback function. Have it read
                            the data, calculate its minimum and maximum,
                            and create a colorscale as follows:
                            """
                        ),
                        html.Code(html.Pre([
                            'pingrid.to_dash_colorscale(pingrid.RAINBOW_COLORMAP)'
                        ])),
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
                            In the config file, add a new entry for the
                            path of the directorty where the data file
                            is, and another entry for the filename.
                            """
                        ),
                        html.P(
                            """
                            Replace all instances of data file reading in
                            maproom.py and layout.py with the strings
                            from config.
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
                            with X, Y and T dimensions. If you have
                            access to some, get new data for your
                            country of interest. To make best use of the
                            rest of the Tutorial, get 10 years of
                            monthly data. Once you have such a file,
                            overwrite your configuration with the new
                            data sources. Don't commit data files to
                            git. git is a code version control tool, not
                            a place to store data. The NY CRU data is a
                            small sample to allow the Tutorialto stand
                            alone. Store your data files somewhere
                            readable.
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
                            Get temperature data from the same source
                            you just got new precipitation data (or
                            continue to work with the NY CRU data). Save
                            the data file in same place as precipitation
                            one and indicate the name of the temperature
                            file in the config.
                            """
                        ),
                        html.P(
                            """
                            In the layout, go back to the dropdown menu
                            we set up for precipitation and add a
                            temperature option.
                            """
                        ),
                        html.P(
                            """
                            In maproom.py, use if/else commands to use
                            the right data file based on the value of
                            the dropdown choice. Note that we are also
                            reading the precipitation file in the
                            layout, but that is just to get lon and lat
                            information. Here we assume both variables
                            will come from the same set and thus have same lat/lon. So we are not changing the data reading in the layout.
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
                            Study how the ticks of the precipitation
                            colorscale are set up and adapt the temperature one to be more useful.
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
                            that picks values of the time dimension of
                            your climatology so that we can select
                            months.
                            """
                        ),
                        html.P(
                            """
                            In maproom, instead of picking the last month of data, pick the month chosen in the
                            layout of the climatological data. Remember
                            to do so for the map and the colorsacle. You
                            will have to pass the dropdown menu momth
                            value in functions and callbacks. Remember also the special case of the map that has a
                            function to create the tiles and another to
                            create the tiles URLs.
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
                            We finished our map now. Let's create a
                            callback for the map title to indicate the
                            variable and month being mapped. The map title is currently defined at the beginning
                            of the map layout.
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
                            add, after out text describing the Maproom,
                            the type-in controls as another mean to input
                            latitude and longitude. We will use our UI
                            component Block to make sure they keep tight
                            together in the app. Below is an example
                            adding the latitude control. Add that and
                            include in another Col in the Block a control
                            for longitude.
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
                            Now that we have our Marker and control
                            ready, in maproom, create a callback that
                            outputs: loc_marker's postion, lat_input's
                            value, lng_input's value; and that takes as
                            inputs: submit_lat_lng's n_clicks, map's
                            click_lat_lng; and lat_input's value,
                            lng_input's value as State. Define the
                            callback function and starts by reading the
                            data. Note that hear, we just need the
                            lat/lon data so we just need the data
                            reading, we need not make additional
                            computations. Once you've read the data,
                            complete the function with the following
                            code:
                            """
                        ),
                        html.Code(html.Pre([
                            '    if dash.ctx.triggered_id == None:',
                            html.Br(),
                            '        lat = data["Y"][int(data["Y"].size/2)].values',
                            html.Br(),
                            '        lng = data["X"][int(data["X"].size/2)].values',
                            html.Br(),
                            '    else:',
                            html.Br(),
                            '        if dash.ctx.triggered_id == "map":',
                            html.Br(),
                            '            lat = click_lat_lng[0]',
                            html.Br(),
                            '            lng = click_lat_lng[1]',
                            html.Br(),
                            '        else:',
                            html.Br(),
                            '            lat = latitude',
                            html.Br(),
                            '            lng = longitude',
                            html.Br(),
                            '        try:',
                            html.Br(),
                            '            nearest_grid = pingrid.sel_snap(data, lat, lng)',
                            html.Br(),
                            '            lat = nearest_grid["Y"].values',
                            html.Br(),
                            '            lng = nearest_grid["X"].values',
                            html.Br(),
                            '        except KeyError:',
                            html.Br(),
                            '            lat = lat',
                            html.Br(),
                            '            lng = lng',
                            html.Br(),
                            '    return [lat, lng], lat, lng'
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
            html.Details(
                [
                    html.Summary("Lesson 17: Plot Local Climatology"),
                    html.Div([
                        html.P(
                            """
                            Now that we can get a specific location from
                            the map, we can plot the climatology for that
                            very location. We're going to plot that under
                            the map. Insert the following Row component
                            as a new Row under the map in the main layout:
                            """
                        ),
                        html.Code(html.Pre([
                            'dbc.Row(',
                            html.Br(),
                            '    [',
                            html.Br(),
                            '        dbc.Col(',
                            html.Br(),
                            '            local_layout(),',
                            html.Br(),
                            '            width=12,',
                            html.Br(),
                            '            style={',
                            html.Br(),
                            '                "background-color": "white",',
                            html.Br(),
                            '                "min-height": "100px",',
                            html.Br(),
                            '                "border-style": "solid",',
                            html.Br(),
                            '                "border-color": "lightGray",',
                            html.Br(),
                            '                "border-width": "1px 0px 0px 0px",',
                            html.Br(),
                            '            },',
                            html.Br(),
                            '        ),',
                            html.Br(),
                            '    ],',
                            html.Br(),
                            '    style={',
                            html.Br(),
                            '        "overflow":"scroll","height":"55%"',
                            html.Br(),
                            '    },',
                            html.Br(),
                            '    className="g-0",',
                            html.Br(),
                            '),',
                        ])),
                        html.P(
                            """
                            You can see that this relies on a new layout
                            component called local_layout. Let set that
                            one up with the following definition:
                            """
                        ),
                        html.Code(html.Pre([
                            'def local_layout():',
                            html.Br(),
                            '    return html.Div(',
                            html.Br(),
                            '        [',
                            html.Br(),
                            '            dbc.Tabs(',
                            html.Br(),
                            '                [',
                            html.Br(),
                            '                    dbc.Tab(',
                            html.Br(),
                            '                        [',
                            html.Br(),
                            '                            dbc.Spinner(dcc.Graph(id="clim_plot")),',
                            html.Br(),
                            '                        ],',
                            html.Br(),
                            '                        label="Monthly Climatology",',
                            html.Br(),
                            '                    ),',
                            html.Br(),
                            '                ],',
                            html.Br(),
                            '                className="mt-4",',
                            html.Br(),
                            '            ),',
                            html.Br(),
                            '        ],',
                            html.Br(),
                            '    )',
                        ])),
                        html.P(
                            """
                            And now you can see that this layout component relies on the id clim_plot where
                            we need to create our dcc Graph.
                            """
                        ),
                        html.P(
                            """
                            Create a callback that outputs clim_plot as a
                            figure, and takes as inputs the poistion of
                            loc_marker and the value of variable.
                            """
                        ),
                        html.P(
                            """
                            Start by reading the data and compute its
                            climatology. Then use our pingrid sel_snap to
                            select the data for the chosen location. Here
                            is a reminder of sel_snap syntax:
                            """
                        ),
                        html.Code(html.Pre([
                            'data = pingrid.sel_snap(data, lat, lng)'
                        ])),
                        html.P(
                            """
                            Then we want to indicate what the x-axis are,
                            for instance with:
                            """
                        ),
                        html.Code(html.Pre([
                            'months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",',
                            html.Br(),
                            '          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]',
                        ])),
                        html.P(
                            """
                            And finally we want to return a bar plot,
                            here is an example of what it could look like
                            using plotly.express library:
                            """
                        ),
                        html.Code(html.Pre([
                            'bar_plot = px.bar(',
                            html.Br(),
                            '    data, x=months, y=data,',
                            html.Br(),
                            '    title = f"{variable} monthly climatology",',
                            html.Br(),
                            '    labels = {',
                            html.Br(),
                            '        "x": "Time (months)",',
                            html.Br(),
                            '        "y": f"{variable} ({data.attrs["units"]})",',
                            html.Br(),
                            '    },',
                            html.Br(),
                            ')',
                        ])),
                        html.P(
                            """
                            When you are done, commit your changes
                            and move on to Lesson 18.
                            """
                        ),
                    ]),
                ],
            ),
        ],
    )