"""
The `layout.py` file is used to def a layout function, which is called within the main maproom.py file where the maproom is run.

The `layout()` function includes any code which defines the layout of the maproom. It should not include any callbacks or directly reference
the data be loaded into the maproom.
"""

# Import libraries used
import os
import dash
from dash import html
import dash_leaflet as dlf
import dash_bootstrap_components as dbc
import ui_components # Import `ui_components.py` which has UI controls tailored to maprooms.
import xarray as xr

import pingrid
CONFIG = pingrid.load_config(os.environ["CONFIG"])

#load in a data file to get initialization info for lat/lng
data_init = xr.open_dataarray(f"{CONFIG['data_dir']}/{(list(CONFIG['vars'].values()))[0]}.nc", decode_times=False)

center_of_the_map = [((data_init["Y"][int(data_init["Y"].size/2)].values)), ((data_init["X"][int(data_init["X"].size/2)].values))]

def layout(): # Defining the function that will be called in the layout section of  `maproom.py`.
    return dbc.Container([ # The function will return the dash bootstrap container, and all of its contents.
       dbc.Row(html.H1(CONFIG["map_title"])), # First of two rows (horizontal) which is the title bar of the maproom.

       dbc.Row([ # second of two rows (horizontal), which contains the rest of the maproom (the map and controls column).

           dbc.Col( # Now we divide the second row into two columns. The first column contains the controls.
               [
         # Within the controls column, we add four `Blocks` which are the controls themselves.
               ui_components.Block( # This block has title 'Variable' and includes a dropdown with the options listed
                 "Variable", ui_components.Select("Variable",["Rainfall","Maximum Temperature","Minimum Temperature","Mean Temperature"])
               ),
               ui_components.Block( # Block containing dropdown to select from months of the year.
                  "Month", ui_components.Month("mon0","jan")
               ),

                ui_components.Block( # Block containing dropdown to select which level to spatially average data over.
                    "Spatially Average Over", ui_components.Select("Spatially Average Over",["National","Council","District",]),
                    html.Span(ui_components.Select("region", ["",]), id="region-container", hidden=True) # Referenced in `set_region()` callback in `maproom.py`
                ),                                                                                 # element will only show if 'council' or 'district' is selected
                                                                                  # Otherwise element will be hidden
           ], width=4), # End of first column; width defined here determines the width of the column.
           dbc.Col( # The second of two columns. This column contains the map.
                dbc.Container( # Container that holds the leaflet map element.
                    [ # This list holds all of the children elements within the container.
                        dlf.Map( # Dash leaflet map.
                            [
                                dlf.LayersControl( # Defining the layers control for the map. Includes both the base map layer options
                                    [              # and the polygon, raster layers. These are all displayed in the layers control button on the map.
                                        dlf.BaseLayer( # Base layers are the map base and can only have one selected at a time in the maproom.
                                            dlf.TileLayer(
                                                url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png", # Cartodb street map.
                                            ),
                                            name="Street",
                                            checked=True,
                                        ),
                                        dlf.BaseLayer(
                                            dlf.TileLayer(
                                                url="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png" # opentopomap topography map.
                                            ),
                                            name="Topo",
                                            checked=False,
                                        ),
                                        dlf.Overlay( # Overlay layers are layers displayed on top of the base layer,
                                            dlf.TileLayer( # and can allow more than one layer to be selected at once.
                                                opacity=.8,
                                                id="map_raster",
                                            ),
                                            name="Raster",
                                            checked=True,
                                        ),
                                        dlf.Overlay([
                                            dlf.GeoJSON(
                                                id="map_borders",
                                                data={"features": []},
                                                options={
                                                    "fill": False,
                                                    "color": "black",
                                                    "weight": .25,
                                                },
                                            ),
                                            dlf.Polygon(
                                                id="map_selected",
                                                positions={"features": []}, #throwing an error because it needs to be initialied with data
                                            ),
                                            ],
                                            name="Borders",
                                            checked=True,
                                        ),
                                    ],
                                    position="topleft", # Where the layers control button is placed.
                                    id="map_layers_control",
                                ),
                                dlf.ScaleControl(imperial=False, position="topright"), # Define scale bar
                                dlf.Colorbar( # Define map color bar
                                    id="map_colorbar",
                                    min=0,
                                    position="bottomleft",
                                    width=300,
                                    height=10,
                                    opacity=.7,
                                ),
                            ],
                            id="map", # Finishing defining the dlf Map element.
                            style={ # The css style applied to the map
                                "width": "100%",
                                "height": "50vh",
                            },
                            center=center_of_the_map, # Where the center of the map will be upon loading the maproom.
                            zoom=8,
                        ),
                    ],
                    fluid=True,
                    style={"padding": "0rem"},
                )
           ),
       ]),
 ])