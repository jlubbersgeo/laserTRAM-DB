#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 13:57:37 2021

The source code for the LaserTRAM-DB dashboard.
https://github.com/jlubbersgeo/laserTRAM-DB

Created and maintained by:
Jordan Lubbers
jlubbers@usgs.gov



"""

import base64
import io
import webbrowser as web

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Input, Output, State, dash_table, dcc, exceptions, html
from plotly.subplots import make_subplots

from lasertram import LaserCalc, LaserTRAM, batch

# this should hopefully be enough colors. Repeats after 48...
colorlist = [
    "#2E91E5",
    "#E15F99",
    "#1CA71C",
    "#FB0D0D",
    "#DA16FF",
    "#222A2A",
    "#B68100",
    "#750D86",
    "#EB663B",
    "#511CFB",
    "#00A08B",
    "#FB00D1",
    "#FC0080",
    "#B2828D",
    "#6C7C32",
    "#778AAE",
    "#862A16",
    "#A777F1",
    "#620042",
    "#1616A7",
    "#DA60CA",
    "#6C4516",
    "#0D2A63",
    "#AF0038",
    "#FD3216",
    "#00FE35",
    "#6A76FC",
    "#FED4C4",
    "#FE00CE",
    "#0DF9FF",
    "#F6F926",
    "#FF9616",
    "#479B55",
    "#EEA6FB",
    "#DC587D",
    "#D626FF",
    "#6E899C",
    "#00B5F7",
    "#B68E00",
    "#C9FBE5",
    "#FF0092",
    "#22FFA7",
    "#E3EE9E",
    "#86CE00",
    "#BC7196",
    "#7E7DCD",
    "#FC6955",
    "#E48F72",
    "#2E91E5",
    "#E15F99",
    "#1CA71C",
    "#FB0D0D",
    "#DA16FF",
    "#222A2A",
    "#B68100",
    "#750D86",
    "#EB663B",
    "#511CFB",
    "#00A08B",
    "#FB00D1",
    "#FC0080",
    "#B2828D",
    "#6C7C32",
    "#778AAE",
    "#862A16",
    "#A777F1",
    "#620042",
    "#1616A7",
    "#DA60CA",
    "#6C4516",
    "#0D2A63",
    "#AF0038",
    "#FD3216",
    "#00FE35",
    "#6A76FC",
    "#FED4C4",
    "#FE00CE",
    "#0DF9FF",
    "#F6F926",
    "#FF9616",
    "#479B55",
    "#EEA6FB",
    "#DC587D",
    "#D626FF",
    "#6E899C",
    "#00B5F7",
    "#B68E00",
    "#C9FBE5",
    "#FF0092",
    "#22FFA7",
    "#E3EE9E",
    "#86CE00",
    "#BC7196",
    "#7E7DCD",
    "#FC6955",
    "#E48F72",
]


# styling the tabls
tabs_styles = {"height": "44px"}
tab_style = {
    "borderBottom": "1px solid #d6d6d6",
    "padding": "6px",
    "fontWeight": "bold",
}

tab_selected_style = {
    "borderTop": "1px solid #d6d6d6",
    "borderBottom": "1px solid #d6d6d6",
    "backgroundColor": "#2c3e50",
    "color": "white",
    "padding": "6px",
}

card_color = "secondary"


web.open_new_tab("http://127.0.0.1:8049/")

app = dash.Dash(__name__)
# app.css.config.serve_locally = True
formtext_color = "secondary"
server = app.server

# the layout of the entire app
app.layout = html.Div(
    [
        dcc.Tabs(
            [
                dcc.Tab(
                    label="LaserTRAM spot",
                    style=tab_style,
                    selected_style=tab_selected_style,
                    children=[
                        dcc.Tabs(
                            [
                                dcc.Tab(
                                    label="New Project",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                    children=[
                                        dbc.Spinner(
                                            children=[dcc.Store(id="stored_data")],
                                            fullscreen=True,
                                            size="lg",
                                            color=tab_selected_style["backgroundColor"],
                                            spinner_style={
                                                "min-height": "500px",
                                                "min-width": "500px",
                                            },
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.H2("LaserTRAM"),
                                                            ]
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                html.H4(
                                                                    "Laser Time Resolved Analysis Module for LA-ICP-MS"
                                                                ),
                                                            ]
                                                        ),
                                                    ],
                                                    align="center",
                                                ),
                                                dbc.Card(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        dcc.Upload(
                                                                            id="upload-data",
                                                                            children=dbc.Button(
                                                                                "Upload Data",
                                                                                id="upload-btn",
                                                                                color="dark",
                                                                                size="lg",
                                                                                n_clicks=0,
                                                                            ),
                                                                        ),
                                                                    ],
                                                                    width=2,
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dbc.Row(
                                                                            [
                                                                                dbc.Col(
                                                                                    [
                                                                                        dbc.Label(
                                                                                            "Spot:"
                                                                                        ),
                                                                                        dcc.Dropdown(
                                                                                            id="spot_dropdown",
                                                                                            multi=False,
                                                                                            style={
                                                                                                "color": "#212121",
                                                                                                "background-color": "none",
                                                                                                "width": "100%",
                                                                                            },
                                                                                            placeholder="Please choose a spot",
                                                                                            value=None,
                                                                                        ),
                                                                                    ]
                                                                                ),
                                                                                dbc.Col(
                                                                                    [
                                                                                        html.Label(
                                                                                            "Int. Std. "
                                                                                        ),
                                                                                        dcc.Dropdown(
                                                                                            id="int_std_dropdown",
                                                                                            multi=False,
                                                                                            style={
                                                                                                "color": "#212121",
                                                                                                "background-color": "none",
                                                                                                "width": "70%",
                                                                                            },
                                                                                            options=[
                                                                                                {
                                                                                                    "label": "43Ca",
                                                                                                    "value": "43Ca",
                                                                                                },
                                                                                                {
                                                                                                    "label": "47Ti",
                                                                                                    "value": "47Ti",
                                                                                                },
                                                                                                {
                                                                                                    "label": "29Si",
                                                                                                    "value": "29Si",
                                                                                                },
                                                                                            ],
                                                                                            value="29Si",
                                                                                        ),
                                                                                    ]
                                                                                ),
                                                                            ]
                                                                        )
                                                                    ],
                                                                    width=4,
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dbc.Row(
                                                                            [
                                                                                dbc.Col(
                                                                                    [
                                                                                        html.Label(
                                                                                            "Save Analysis to Export:"
                                                                                        ),
                                                                                        html.Br(),
                                                                                        dbc.Button(
                                                                                            "Record &\n Next",
                                                                                            id="record_btn",
                                                                                            color="success",
                                                                                            size="lg",
                                                                                            n_clicks=0,
                                                                                        ),
                                                                                    ]
                                                                                ),
                                                                                dbc.Col(
                                                                                    [
                                                                                        html.Label(
                                                                                            "Skip analysis:"
                                                                                        ),
                                                                                        html.Br(),
                                                                                        dbc.Button(
                                                                                            "Skip to Next",
                                                                                            id="skip_btn",
                                                                                            color="warning",
                                                                                            size="lg",
                                                                                            n_clicks=0,
                                                                                        ),
                                                                                    ]
                                                                                ),
                                                                                # dbc.Col(
                                                                                #     [
                                                                                #         html.Label(
                                                                                #             "Despike:"
                                                                                #         ),
                                                                                #         dcc.Dropdown(
                                                                                #             id="despike_dropdown",
                                                                                #             multi=False,
                                                                                #             style={
                                                                                #                 "color": "#212121",
                                                                                #                 "background-color": "none",
                                                                                #                 "width": "70%",
                                                                                #             },
                                                                                #             options=[
                                                                                #                 {
                                                                                #                     "label": "None",
                                                                                #                     "value": "None",
                                                                                #                 },
                                                                                #                 {
                                                                                #                     "label": "all",
                                                                                #                     "value": "all",
                                                                                #                 },
                                                                                #             ],
                                                                                #             value=None,
                                                                                #         ),
                                                                                #     ]
                                                                                # ),
                                                                            ]
                                                                        ),
                                                                    ],
                                                                    width=4,
                                                                ),
                                                            ],
                                                        )
                                                    ],
                                                    body=True,
                                                    style={"width": "100rem"},
                                                    color="secondary",
                                                    inverse=True,
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                html.H4(
                                                                                    "Choose background and interval of interest with the sliders"
                                                                                ),
                                                                                html.Hr(),
                                                                                dbc.Row(
                                                                                    [
                                                                                        dbc.Col(
                                                                                            [
                                                                                                dcc.RangeSlider(
                                                                                                    id="interval_slider",
                                                                                                    min=0,
                                                                                                    max=60,
                                                                                                    value=[
                                                                                                        5,
                                                                                                        15,
                                                                                                        25,
                                                                                                        45,
                                                                                                    ],
                                                                                                    marks=None,
                                                                                                    tooltip={
                                                                                                        "always_visible": True,
                                                                                                        "placement": "bottom",
                                                                                                    },
                                                                                                    allowCross=False,
                                                                                                ),
                                                                                            ]
                                                                                        ),
                                                                                        dbc.Col(
                                                                                            []
                                                                                        ),
                                                                                    ]
                                                                                ),
                                                                            ],
                                                                        ),
                                                                    ]
                                                                ),
                                                                dcc.Graph(
                                                                    id="raw-data",
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        html.Div(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        html.H4(
                                                                            "Analyte Uncertainties"
                                                                        ),
                                                                        dcc.Graph(
                                                                            id="error-data",
                                                                            style={
                                                                                "width": "90vh"
                                                                            },
                                                                        ),
                                                                    ]
                                                                )
                                                            ],
                                                            style={
                                                                "width": "50%",
                                                                "display": "inline-block",
                                                            },
                                                        ),
                                                        html.Div(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        html.H4(
                                                                            "Saved Spot Data"
                                                                        ),
                                                                        dash_table.DataTable(
                                                                            id="adding-rows-table",
                                                                            columns=[
                                                                                {
                                                                                    "name": "analyte-{}".format(
                                                                                        i
                                                                                    ),
                                                                                    "id": "analyte-{}".format(
                                                                                        i
                                                                                    ),
                                                                                    "deletable": True,
                                                                                    "renamable": False,
                                                                                }
                                                                                for i in range(
                                                                                    1, 5
                                                                                )
                                                                            ],
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "height": 275,
                                                                                "width": "70vh",
                                                                            },
                                                                            fixed_rows={
                                                                                "headers": True
                                                                            },
                                                                            style_cell={
                                                                                # all three widths are needed
                                                                                "minWidth": "100px",
                                                                                "width": "60px",
                                                                                "maxWidth": "60px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                                "textAlign": "center",
                                                                            },
                                                                            style_data_conditional=[
                                                                                {
                                                                                    "if": {
                                                                                        "row_index": "odd"
                                                                                    },
                                                                                    "backgroundColor": "rgb(248, 248, 248)",
                                                                                }
                                                                            ],
                                                                            style_header={
                                                                                "backgroundColor": "rgb(230, 230, 230)",
                                                                                "fontWeight": "bold",
                                                                                "textAlign": "center",
                                                                            },
                                                                            data=[
                                                                                {
                                                                                    "analyte-{}".format(
                                                                                        i
                                                                                    ): (
                                                                                        (
                                                                                            i
                                                                                            - 1
                                                                                        )
                                                                                        * 5
                                                                                    )
                                                                                    for i in range(
                                                                                        1,
                                                                                        5,
                                                                                    )
                                                                                }
                                                                            ],
                                                                            editable=True,
                                                                            row_deletable=False,
                                                                            export_format="xlsx",
                                                                            export_headers="display",
                                                                        ),
                                                                    ]
                                                                )
                                                            ],
                                                            style={
                                                                "width": "50%",
                                                                "display": "inline-block",
                                                            },
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                                dcc.Tab(
                                    label="Re-processing",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                    children=[
                                        dcc.Store(id="stored_new_data"),
                                        dcc.Store(id="stored_old_data"),
                                        dbc.Col(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.H2(
                                                                    "LaserTRAM Re-processing"
                                                                ),
                                                            ]
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                html.H4(
                                                                    "Re-process an old experiment using a new internal standard"
                                                                ),
                                                            ]
                                                        ),
                                                    ],
                                                    align="center",
                                                ),
                                                dbc.Card(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        dcc.Upload(
                                                                            id="upload-data_reprocess",
                                                                            children=dbc.Button(
                                                                                "Upload old LT file",
                                                                                id="upload-btn_reprocess",
                                                                                color="dark",
                                                                                size="lg",
                                                                                n_clicks=0,
                                                                            ),
                                                                        ),
                                                                        html.Hr(),
                                                                    ],
                                                                    width=2,
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dbc.Row(
                                                                            [
                                                                                dbc.Col(
                                                                                    [
                                                                                        dbc.Label(
                                                                                            "Internal Standard:"
                                                                                        ),
                                                                                        dcc.Dropdown(
                                                                                            id="int_std_dropdown_reprocess",
                                                                                            multi=False,
                                                                                            style={
                                                                                                "color": "#212121",
                                                                                                "background-color": "none",
                                                                                                "width": "100%",
                                                                                            },
                                                                                            placeholder="Choose a new internal standard",
                                                                                            value=None,
                                                                                        ),
                                                                                    ]
                                                                                ),
                                                                            ]
                                                                        )
                                                                    ],
                                                                    width=4,
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dbc.Row(
                                                                            [
                                                                                dbc.Col(),
                                                                                dbc.Col(
                                                                                    [
                                                                                        dbc.Button(
                                                                                            "Re-process!",
                                                                                            id="reprocess_btn",
                                                                                            color="success",
                                                                                            size="lg",
                                                                                            n_clicks=0,
                                                                                        ),
                                                                                    ]
                                                                                ),
                                                                            ]
                                                                        ),
                                                                    ],
                                                                    width=4,
                                                                ),
                                                            ],
                                                        )
                                                    ],
                                                    body=True,
                                                    style={"width": "100rem"},
                                                    color=card_color,
                                                    inverse=True,
                                                ),
                                                dbc.Row(
                                                    [
                                                        html.Div(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        html.H4(
                                                                            "Old normalized ratios "
                                                                        ),
                                                                        dash_table.DataTable(
                                                                            id="old_data_table",
                                                                            columns=[
                                                                                {
                                                                                    "name": "Spot",
                                                                                    "id": "Spot",
                                                                                    "renamable": False,
                                                                                },
                                                                                {
                                                                                    "name": "bkgd_start",
                                                                                    "id": "bkgd_start",
                                                                                    "renamable": False,
                                                                                },
                                                                                {
                                                                                    "name": "bkgd_stop",
                                                                                    "id": "bkgd_stop",
                                                                                    "renamable": False,
                                                                                },
                                                                                {
                                                                                    "name": "int_start",
                                                                                    "id": "int_start",
                                                                                    "renamable": False,
                                                                                },
                                                                                {
                                                                                    "name": "int_stop",
                                                                                    "id": "int_stop",
                                                                                    "renamable": False,
                                                                                },
                                                                                {
                                                                                    "name": "norm",
                                                                                    "id": "norm",
                                                                                    "renamable": False,
                                                                                },
                                                                                {
                                                                                    "name": "norm_cps",
                                                                                    "id": "norm_cps",
                                                                                    "renamable": False,
                                                                                },
                                                                            ]
                                                                            + [
                                                                                {
                                                                                    "name": "analyte-{}".format(
                                                                                        i
                                                                                    ),
                                                                                    "id": "analyte-{}".format(
                                                                                        i
                                                                                    ),
                                                                                    "renamable": False,
                                                                                }
                                                                                for i in range(
                                                                                    1,
                                                                                    10,
                                                                                )
                                                                            ],
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "height": 400,
                                                                                "width": "90vh",
                                                                            },
                                                                            fixed_rows={
                                                                                "headers": True
                                                                            },
                                                                            style_cell={
                                                                                # all three widths are needed
                                                                                "minWidth": "100px",
                                                                                "width": "60px",
                                                                                "maxWidth": "60px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                                "textAlign": "center",
                                                                            },
                                                                            style_data_conditional=[
                                                                                {
                                                                                    "if": {
                                                                                        "row_index": "odd"
                                                                                    },
                                                                                    "backgroundColor": "rgb(248, 248, 248)",
                                                                                }
                                                                            ],
                                                                            style_header={
                                                                                "backgroundColor": "rgb(230, 230, 230)",
                                                                                "fontWeight": "bold",
                                                                                "textAlign": "center",
                                                                            },
                                                                            data=[
                                                                                {
                                                                                    "analyte-{}".format(
                                                                                        i
                                                                                    ): (
                                                                                        (
                                                                                            i
                                                                                            - 1
                                                                                        )
                                                                                        * 5
                                                                                    )
                                                                                    for i in range(
                                                                                        1,
                                                                                        5,
                                                                                    )
                                                                                }
                                                                            ],
                                                                            editable=True,
                                                                            row_deletable=False,
                                                                            export_format="xlsx",
                                                                            export_headers="display",
                                                                        ),
                                                                    ],
                                                                )
                                                            ],
                                                            style={
                                                                "width": "50%",
                                                                "display": "inline-block",
                                                            },
                                                        ),
                                                        html.Div(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        html.H4(
                                                                            children=[
                                                                                "Re-normalized data",
                                                                                html.Div(
                                                                                    id="reprocess_header",
                                                                                    style={
                                                                                        "display": "inline"
                                                                                    },
                                                                                ),
                                                                            ]
                                                                        ),
                                                                        dash_table.DataTable(
                                                                            id="new_data_table",
                                                                            columns=[
                                                                                {
                                                                                    "name": "Spot",
                                                                                    "id": "Spot",
                                                                                    "renamable": False,
                                                                                },
                                                                                {
                                                                                    "name": "bkgd_start",
                                                                                    "id": "bkgd_start",
                                                                                    "renamable": False,
                                                                                },
                                                                                {
                                                                                    "name": "bkgd_stop",
                                                                                    "id": "bkgd_stop",
                                                                                    "renamable": False,
                                                                                },
                                                                                {
                                                                                    "name": "int_start",
                                                                                    "id": "int_start",
                                                                                    "renamable": False,
                                                                                },
                                                                                {
                                                                                    "name": "int_stop",
                                                                                    "id": "int_stop",
                                                                                    "renamable": False,
                                                                                },
                                                                                {
                                                                                    "name": "norm",
                                                                                    "id": "norm",
                                                                                    "renamable": False,
                                                                                },
                                                                                {
                                                                                    "name": "norm_cps",
                                                                                    "id": "norm_cps",
                                                                                    "renamable": False,
                                                                                },
                                                                            ]
                                                                            + [
                                                                                {
                                                                                    "name": "analyte-{}".format(
                                                                                        i
                                                                                    ),
                                                                                    "id": "analyte-{}".format(
                                                                                        i
                                                                                    ),
                                                                                    "renamable": False,
                                                                                }
                                                                                for i in range(
                                                                                    1,
                                                                                    10,
                                                                                )
                                                                            ],
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "height": 400,
                                                                                "width": "90vh",
                                                                            },
                                                                            fixed_rows={
                                                                                "headers": True
                                                                            },
                                                                            style_cell={
                                                                                # all three widths are needed
                                                                                "minWidth": "100px",
                                                                                "width": "60px",
                                                                                "maxWidth": "60px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                                "textAlign": "center",
                                                                            },
                                                                            style_data_conditional=[
                                                                                {
                                                                                    "if": {
                                                                                        "row_index": "odd"
                                                                                    },
                                                                                    "backgroundColor": "rgb(248, 248, 248)",
                                                                                }
                                                                            ],
                                                                            style_header={
                                                                                "backgroundColor": "rgb(230, 230, 230)",
                                                                                "fontWeight": "bold",
                                                                                "textAlign": "center",
                                                                            },
                                                                            data=[
                                                                                {
                                                                                    "analyte-{}".format(
                                                                                        i
                                                                                    ): (
                                                                                        (
                                                                                            i
                                                                                            - 1
                                                                                        )
                                                                                        * 5
                                                                                    )
                                                                                    for i in range(
                                                                                        1,
                                                                                        5,
                                                                                    )
                                                                                }
                                                                            ],
                                                                            editable=True,
                                                                            row_deletable=False,
                                                                            export_format="xlsx",
                                                                            export_headers="display",
                                                                        ),
                                                                    ],
                                                                )
                                                            ],
                                                            style={
                                                                "width": "50%",
                                                                "display": "inline-block",
                                                            },
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                            ]
                        ),
                    ],
                ),
                dcc.Tab(
                    label="LaserTRAM profiler",
                    style=tab_style,
                    selected_style=tab_selected_style,
                    children=[
                        dcc.Store(id="stored_data_p"),
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H2("LaserTRAM profiler"),
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                html.H4(
                                                    "Reducing line of spots data for LA-ICP-MS"
                                                ),
                                            ]
                                        ),
                                    ],
                                    align="center",
                                ),
                                dbc.Card(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dcc.Upload(
                                                            id="upload-data_p",
                                                            children=dbc.Button(
                                                                "Upload Data",
                                                                id="upload-btn_p",
                                                                color="dark",
                                                                size="lg",
                                                                n_clicks=0,
                                                            ),
                                                        ),
                                                        html.Hr(),
                                                    ],
                                                    width=1,
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Label("Int. Std. "),
                                                        dcc.Dropdown(
                                                            id="int_std_dropdown_p",
                                                            multi=False,
                                                            style={
                                                                "color": "#212121",
                                                                "background-color": "none",
                                                                "width": "70%",
                                                            },
                                                            options=[
                                                                {
                                                                    "label": "43Ca",
                                                                    "value": "43Ca",
                                                                },
                                                                {
                                                                    "label": "47Ti",
                                                                    "value": "47Ti",
                                                                },
                                                                {
                                                                    "label": "29Si",
                                                                    "value": "29Si",
                                                                },
                                                            ],
                                                            value="43Ca",
                                                        ),
                                                    ],
                                                    width=2,
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Label("Step Size (sec)"),
                                                        dcc.Input(
                                                            id="step_val_p",
                                                            type="number",
                                                            value=10,
                                                        ),
                                                    ],
                                                    width=2,
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Label(
                                                            "Control Step Direction Here"
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    dbc.Button(
                                                                        "Backwards",
                                                                        id="back_btn_p",
                                                                        color="warning",
                                                                        size="lg",
                                                                        n_clicks=0,
                                                                    ),
                                                                ),
                                                                dbc.Col(
                                                                    dbc.Button(
                                                                        "Forwards",
                                                                        id="forward_btn_p",
                                                                        color="info",
                                                                        size="lg",
                                                                        n_clicks=0,
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                    ],
                                                    width=3,
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Label(
                                                            "Record each individual spot"
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                dbc.Button(
                                                                    "Record Spot",
                                                                    id="record_btn_p",
                                                                    color="success",
                                                                    size="lg",
                                                                    n_clicks=0,
                                                                )
                                                            ]
                                                        ),
                                                    ],
                                                    width=2,
                                                ),
                                            ]
                                        )
                                    ],
                                    body=True,
                                    style={"width": "100rem"},
                                    color="secondary",
                                    inverse=True,
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.H4(
                                                                    "Choose background and interval of interest with the sliders"
                                                                ),
                                                                html.Hr(),
                                                                dcc.RangeSlider(
                                                                    id="interval_slider_p",
                                                                    step=1,
                                                                    value=[
                                                                        2,
                                                                        12,
                                                                        15,
                                                                        25,
                                                                    ],
                                                                    tooltip={
                                                                        "always_visible": True,
                                                                        "placement": "bottom",
                                                                    },
                                                                    allowCross=False,
                                                                ),
                                                            ],
                                                        ),
                                                    ]
                                                ),
                                                dcc.Graph(
                                                    id="raw-data_p",
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H4("Analyte Uncertainties"),
                                                dcc.Graph(
                                                    id="error-data_p",
                                                    style={"width": "100vh"},
                                                ),
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                html.H4("Saved Spot Data"),
                                                dash_table.DataTable(
                                                    id="adding-rows-table_p",
                                                    columns=[
                                                        {
                                                            "name": "analyte-{}".format(
                                                                i
                                                            ),
                                                            "id": "analyte-{}".format(
                                                                i
                                                            ),
                                                            "deletable": True,
                                                            "renamable": False,
                                                        }
                                                        for i in range(1, 5)
                                                    ],
                                                    style_table={
                                                        "overflowX": "auto",
                                                        "height": 275,
                                                        "width": "80vh",
                                                    },
                                                    fixed_rows={"headers": True},
                                                    style_cell={
                                                        # all three widths are needed
                                                        "minWidth": "100px",
                                                        "width": "60px",
                                                        "maxWidth": "60px",
                                                        "overflow": "hidden",
                                                        "textOverflow": "ellipsis",
                                                    },
                                                    style_data_conditional=[
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248, 248, 248)",
                                                        }
                                                    ],
                                                    style_header={
                                                        "backgroundColor": "rgb(230, 230, 230)",
                                                        "fontWeight": "bold",
                                                    },
                                                    data=[
                                                        {
                                                            "analyte-{}".format(i): (
                                                                (i - 1) * 5
                                                            )
                                                            for i in range(1, 5)
                                                        }
                                                    ],
                                                    editable=True,
                                                    row_deletable=False,
                                                    export_format="xlsx",
                                                    export_headers="display",
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                ),
                dcc.Tab(
                    label="LaserCalc",
                    style=tab_style,
                    selected_style=tab_selected_style,
                    children=[
                        dcc.Tabs(
                            [
                                dcc.Tab(
                                    label="Concentrations data",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                    children=[
                                        # Hidden div inside the app that stores the intermediate value
                                        dcc.Store(id="stored_data_c"),
                                        dcc.Store(id="stored_stds"),
                                        dcc.Store(id="stored_calibstd_data"),
                                        dbc.Col(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.H2("LaserCalc"),
                                                            ]
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                html.H4(
                                                                    "Calculating concentrations for LA-ICP-MS spot data"
                                                                ),
                                                            ]
                                                        ),
                                                    ],
                                                    align="center",
                                                ),
                                                dbc.Card(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        dcc.Upload(
                                                                            id="upload-data_c",
                                                                            children=dbc.Button(
                                                                                "Upload Data",
                                                                                id="upload-btn_c",
                                                                                color="dark",
                                                                                size="lg",
                                                                                n_clicks=0,
                                                                            ),
                                                                        ),
                                                                        html.Hr(),
                                                                        dcc.Upload(
                                                                            id="upload-stds",
                                                                            children=dbc.Button(
                                                                                "Upload Stds",
                                                                                id="stds_btn",
                                                                                color="secondary",
                                                                                size="lg",
                                                                                n_clicks=0,
                                                                            ),
                                                                        ),
                                                                    ],
                                                                    width=2,
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dbc.Row(
                                                                            [
                                                                                dbc.Col(
                                                                                    [
                                                                                        dbc.Label(
                                                                                            "Calibration Standard:"
                                                                                        ),
                                                                                        dcc.Dropdown(
                                                                                            id="std_dropdown",
                                                                                            multi=False,
                                                                                            style={
                                                                                                "color": "#212121",
                                                                                                "background-color": "none",
                                                                                                "width": "100%",
                                                                                            },
                                                                                            placeholder="Choose calibration std.",
                                                                                            value=None,
                                                                                        ),
                                                                                    ]
                                                                                ),
                                                                            ]
                                                                        )
                                                                    ],
                                                                    width=4,
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dbc.Row(
                                                                            [
                                                                                html.Label(
                                                                                    "Drift significance threshold: "
                                                                                ),
                                                                                dcc.Input(
                                                                                    id="drift_alpha",
                                                                                    type="number",
                                                                                    value=0.01,
                                                                                    min=float(
                                                                                        0
                                                                                    ),
                                                                                    max=float(
                                                                                        1
                                                                                    ),
                                                                                    step=float(
                                                                                        0.001
                                                                                    ),
                                                                                ),
                                                                            ]
                                                                        )
                                                                    ],
                                                                    width=2,
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dbc.Row(
                                                                            [
                                                                                dbc.Col(
                                                                                    [
                                                                                        dbc.Button(
                                                                                            "Calculate!",
                                                                                            id="calculate_btn",
                                                                                            color="success",
                                                                                            size="lg",
                                                                                            n_clicks=0,
                                                                                        ),
                                                                                    ]
                                                                                ),
                                                                            ]
                                                                        ),
                                                                    ],
                                                                    width=2,
                                                                ),
                                                            ],
                                                        )
                                                    ],
                                                    body=True,
                                                    style={"width": "100rem"},
                                                    color=card_color,
                                                    inverse=True,
                                                ),
                                                dbc.Row(
                                                    [
                                                        html.Div(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        html.H4(
                                                                            "Internal Std. Concentrations: "
                                                                        ),
                                                                        dash_table.DataTable(
                                                                            id="int_std_table",
                                                                            columns=[
                                                                                {
                                                                                    "name": "Spot",
                                                                                    "id": "Spot",
                                                                                    "renamable": False,
                                                                                },
                                                                            ],
                                                                            style_table={
                                                                                "overflowX": "scroll",
                                                                                "width": "70vh",
                                                                                "height": "90vh",
                                                                            },
                                                                            fixed_rows={
                                                                                "headers": True
                                                                            },
                                                                            style_cell={
                                                                                # all three widths are needed
                                                                                "minWidth": "10px",
                                                                                "width": "10px",
                                                                                "maxWidth": "30px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                                "textAlign": "center",
                                                                            },
                                                                            style_data_conditional=[
                                                                                {
                                                                                    "if": {
                                                                                        "row_index": "odd"
                                                                                    },
                                                                                    "backgroundColor": "rgb(248, 248, 248)",
                                                                                }
                                                                            ],
                                                                            style_header={
                                                                                "backgroundColor": "rgb(230, 230, 230)",
                                                                                "fontWeight": "bold",
                                                                                "textAlign": "center",
                                                                            },
                                                                            editable=True,
                                                                            row_deletable=False,
                                                                        ),
                                                                    ],
                                                                    width=3,
                                                                )
                                                            ],
                                                            style={
                                                                "width": "50%",
                                                                "display": "inline-block",
                                                            },
                                                        ),
                                                        html.Div(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        html.H4(
                                                                            children=[
                                                                                "",
                                                                                html.Div(
                                                                                    id="table_header",
                                                                                    style={
                                                                                        "display": "inline"
                                                                                    },
                                                                                ),
                                                                            ]
                                                                        ),
                                                                        dash_table.DataTable(
                                                                            id="concentrations_table",
                                                                            columns=[
                                                                                {
                                                                                    "name": "Spot",
                                                                                    "id": "Spot",
                                                                                    "renamable": False,
                                                                                },
                                                                                {
                                                                                    "name": "Int. Std. Conc.",
                                                                                    "id": "Int. Std. Conc.",
                                                                                    "renamable": False,
                                                                                },
                                                                                {
                                                                                    "name": "Int. Std. 1 stdev %",
                                                                                    "id": "Int. Std. 1 stdev %",
                                                                                    "renamable": False,
                                                                                },
                                                                            ]
                                                                            + [
                                                                                {
                                                                                    "name": "analyte-{}".format(
                                                                                        i
                                                                                    ),
                                                                                    "id": "analyte-{}".format(
                                                                                        i
                                                                                    ),
                                                                                    "renamable": False,
                                                                                }
                                                                                for i in range(
                                                                                    1,
                                                                                    10,
                                                                                )
                                                                            ],
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "width": "90vh",
                                                                                "height": "90vh",
                                                                            },
                                                                            fixed_rows={
                                                                                "headers": True
                                                                            },
                                                                            style_cell={
                                                                                # all three widths are needed
                                                                                "minWidth": "100px",
                                                                                "width": "60px",
                                                                                "maxWidth": "60px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                                "textAlign": "center",
                                                                            },
                                                                            style_data_conditional=[
                                                                                {
                                                                                    "if": {
                                                                                        "row_index": "odd"
                                                                                    },
                                                                                    "backgroundColor": "rgb(248, 248, 248)",
                                                                                }
                                                                            ],
                                                                            style_header={
                                                                                "backgroundColor": "rgb(230, 230, 230)",
                                                                                "fontWeight": "bold",
                                                                                "textAlign": "center",
                                                                            },
                                                                            data=[
                                                                                {
                                                                                    "analyte-{}".format(
                                                                                        i
                                                                                    ): (
                                                                                        (
                                                                                            i
                                                                                            - 1
                                                                                        )
                                                                                        * 5
                                                                                    )
                                                                                    for i in range(
                                                                                        1,
                                                                                        10,
                                                                                    )
                                                                                }
                                                                            ],
                                                                            editable=True,
                                                                            row_deletable=False,
                                                                            export_format="xlsx",
                                                                            export_headers="display",
                                                                        ),
                                                                    ]
                                                                )
                                                            ],
                                                            style={
                                                                "width": "50%",
                                                                "display": "inline-block",
                                                            },
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                                # Hidden div inside the app that stores the intermediate value
                                dcc.Tab(
                                    label="Primary Standard data",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                    children=[
                                        html.H3("Choose an analyte to inspect!"),
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id="analyte_dropdown",
                                                    multi=False,
                                                    style={
                                                        "color": "#212121",
                                                        "background-color": "none",
                                                        "width": "50%",
                                                    },
                                                    placeholder="Please choose an analyte",
                                                    value=None,
                                                ),
                                                dcc.Graph(id="drift_correct_fig"),
                                                dash_table.DataTable(
                                                    id="calib_std_table",
                                                    columns=[
                                                        {
                                                            "name": "Spot",
                                                            "id": "Spot",
                                                            "renamable": False,
                                                        },
                                                    ]
                                                    + [
                                                        {
                                                            "name": "analyte-{}".format(
                                                                i
                                                            ),
                                                            "id": "analyte-{}".format(
                                                                i
                                                            ),
                                                            "renamable": False,
                                                        }
                                                        for i in range(1, 10)
                                                    ],
                                                    style_table={
                                                        "overflowX": "auto",
                                                        "height": 500,
                                                        # "width": "100vh",
                                                    },
                                                    fixed_rows={"headers": True},
                                                    style_cell={
                                                        # all three widths are needed
                                                        "minWidth": "50px",
                                                        "width": "60px",
                                                        "maxWidth": "100px",
                                                        "overflow": "hidden",
                                                        "textOverflow": "ellipsis",
                                                        "textAlign": "center",
                                                    },
                                                    style_data_conditional=[
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248, 248, 248)",
                                                        }
                                                    ],
                                                    style_header={
                                                        "backgroundColor": "rgb(230, 230, 230)",
                                                        "fontWeight": "bold",
                                                        "textAlign": "center",
                                                    },
                                                    data=[
                                                        {
                                                            "analyte-{}".format(i): (
                                                                (i - 1) * 5
                                                            )
                                                            for i in range(1, 10)
                                                        }
                                                    ],
                                                    editable=True,
                                                    row_deletable=False,
                                                    export_format="xlsx",
                                                    export_headers="display",
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                            ]
                        )
                    ],
                ),
            ]
        ),
    ]
)


text_color = "#000000"


#############################################################################
########################### LASERTRAM TAB ###################################
#############################################################################
# upload data callback
@app.callback(
    [
        Output("stored_data", "data"),
        Output("spot_dropdown", "options"),
        Output("adding-rows-table", "columns"),
        Output("int_std_dropdown", "options"),
        Output("int_std_dropdown", "value"),
        # Output("despike_dropdown", "options"),
        # Output("despike_dropdown", "value"),
    ],
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
)
def get_data(contents, filename):
    if filename == None:
        # arbitrary place holders until data are uploaded
        spot_list = [{"label": "please upload some data", "value": "None"}]
        data = pd.DataFrame()
        columns = [
            {"id": "analyte-{}".format(i), "name": "analyte-{}".format(i)}
            for i in range(1, 5)
        ]
        analyte_list = [{"label": "Choose analyte", "value": "None"}]
        int_std = "None"
        state = False

    elif "xls" in filename:
        # state = True
        content_type, content_string = contents.split(",")

        decoded = base64.b64decode(content_string)
        # Assume that the user uploaded an excel file
        data = pd.read_excel(io.BytesIO(decoded))
        data.dropna(inplace=True)

        data = data.set_index(["SampleLabel"])

        # initial columns
        columns = (
            [{"id": "timestamp", "name": "timestamp"}]
            + [{"id": "Spot", "name": "Spot"}]
            + [{"id": "despiked", "name": "despiked"}]
            + [{"id": "omitted_region", "name": "omitted_region"}]
            + [{"id": "bkgd_start", "name": "bkgd_start"}]
            + [{"id": "bkgd_stop", "name": "bkgd_stop"}]
            + [{"id": "int_start", "name": "int_start"}]
            + [{"id": "int_stop", "name": "int_stop"}]
            + [{"id": "norm", "name": "norm"}]
            + [{"id": "norm_cps", "name": "norm_cps"}]
            + [{"id": c, "name": c} for c in data.iloc[:, 2:].columns]
            + [{"id": c + "_se", "name": c + "_se"} for c in data.iloc[:, 2:].columns]
        )

        spots = list(data.index.unique())
        spot_list = [{"label": spot, "value": spot} for spot in spots]
        analyte_list = [
            {"label": analyte, "value": analyte} for analyte in data.iloc[:, 2:].columns
        ]
        despike_list = [
            {"label": analyte, "value": analyte} for analyte in ["None", "all"]
        ]
        data.reset_index(inplace=True)
        # make 43Ca default internal standard unless it's not there
        # then 29Si...then first column in data if neither are present
        if "43Ca" in data.iloc[:, 1:].columns:
            int_std = "43Ca"

        elif "43Ca" not in data.iloc[:, 1:].columns:
            if "29Si" in data.iloc[:, 1:].columns:
                int_std = "29Si"
        else:
            int_std = list(data.iloc[:, 1:].columns)[0]

        # state = False

    return (
        data.to_json(orient="split"),
        spot_list,
        columns,
        analyte_list,
        int_std,
        # despike_list,
        # "None",
    )


# plotting data callback
@app.callback(
    [
        Output("raw-data", "figure"),
        Output("error-data", "figure"),
        Output("interval_slider", "max"),
    ],
    [
        Input("spot_dropdown", "value"),
        Input("stored_data", "data"),
        Input("interval_slider", "value"),
        Input("int_std_dropdown", "value"),
        # Input("despike_dropdown", "value"),
    ],
    [
        State("upload-data", "filename"),
        State("interval_slider", "max"),
    ],
)
def plot(spot, stored_data, interval_slider, int_std, filename, slider_max):
    # empty if nothing is uploaded
    if filename == None:
        fig = {}
        error_fig = {}

        return fig, error_fig, slider_max

    else:
        # empty if user has not chosen a spot yet
        if spot == None:
            fig = {}
            error_fig = {}

            return fig, error_fig, slider_max
        else:
            # retrieve data stored in background
            data = pd.read_json(stored_data, orient="split")
            data.set_index("SampleLabel", inplace=True)

            # do the lasertram stuff
            current_spot = LaserTRAM(name=spot)
            current_spot.get_data(data.loc[spot, :])
            # if despike == "all":

            #     current_spot.despike_data()

            current_spot.assign_int_std(int_std)
            current_spot.assign_intervals(
                (interval_slider[0], interval_slider[1]),
                (interval_slider[2], interval_slider[3]),
            )
            current_spot.get_bkgd_data()
            current_spot.subtract_bkgd()
            current_spot.get_detection_limits()
            current_spot.normalize_interval()
            current_spot.make_output_report()

            # make the plots
            fig = make_subplots(
                rows=1,
                cols=2,
                horizontal_spacing=0.2,
                specs=[[{"secondary_y": False}, {"secondary_y": False}]],
            )

            fig.add_shape(
                type="rect",
                x0=interval_slider[2],
                y0=100,
                x1=interval_slider[3],
                y1=current_spot.data_matrix.max().max(),
                line_width=0,
                fillcolor="green",
                opacity=0.25,
                row=1,
                col=1,
            )

            fig.add_shape(
                type="rect",
                x0=interval_slider[0],
                y0=100,
                x1=interval_slider[1],
                y1=current_spot.data_matrix.max().max(),
                line_width=0,
                fillcolor="red",
                opacity=0.25,
                row=1,
                col=1,
            )
            for i in range(len(current_spot.analytes)):
                fig.add_trace(
                    go.Scatter(
                        x=current_spot.data["Time"],
                        y=current_spot.data.loc[:, current_spot.analytes[i]],
                        mode="lines",
                        name=current_spot.analytes[i],
                        line=dict(
                            color=colorlist[i],
                        ),
                    ),
                    row=1,
                    col=1,
                )

                fig.add_trace(
                    go.Scatter(
                        x=current_spot.data.loc[
                            :,
                            "Time",
                        ][current_spot.int_start_idx : current_spot.int_stop_idx],
                        y=current_spot.bkgd_subtract_normal_data[:, i],
                        mode="lines",
                        name=current_spot.analytes[i],
                        showlegend=False,
                        line=dict(
                            color=colorlist[i],
                        ),
                    ),
                    row=1,
                    col=2,
                )

            fig.update_layout(
                title=spot,
                template="simple_white",
                font=dict(size=18, color=text_color),
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0
                ),
                autosize=True,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )

            fig.update_yaxes(
                title_text="Counts per second",
                tickcolor=text_color,
                linewidth=2,
                type="log",
                linecolor=text_color,
                row=1,
                col=1,
            )
            fig.update_yaxes(
                title_text="Normalized to {}".format(int_std), type="log", row=1, col=2
            )
            fig.update_xaxes(title_text="Interval Time (s)", row=1, col=2)

            fig.update_xaxes(
                title_text="Time (s)",
                tickcolor=text_color,
                linewidth=2,
                linecolor=text_color,
                row=1,
                col=1,
            )

            # err_colors = [
            #     "gold" if current_spot.bkgd_correct_std_err_rel[x] >= 5 else "green"
            #     for x in range(len(current_spot.bkgd_correct_std_err_rel))
            # ]
            err_colors = []
            for val in current_spot.bkgd_correct_std_err_rel:
                if val > 10:
                    err_colors.append("#ad0013")
                elif (val > 7.5) & (val <= 10):
                    err_colors.append("#fa9d1b")
                elif (val > 5) & (val <= 7.5):
                    err_colors.append("#fac928")
                else:
                    err_colors.append("#2b8f45")

            error_fig = go.Figure(
                go.Bar(
                    x=current_spot.analytes,
                    y=current_spot.bkgd_correct_std_err_rel,
                    marker=dict(color=err_colors),
                    text=current_spot.bkgd_correct_med,
                    textposition="auto",
                )
            )
            error_fig.update_yaxes(title_text="% SE")
            error_fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
            error_fig.update_layout(
                template="simple_white",
                font=dict(size=18, color=text_color),
                height=300,
                uniformtext_minsize=8,
                uniformtext_mode="hide",
            )

            return fig, error_fig, current_spot.data["Time"].max()


# add "recorded" data to table for eventual export
@app.callback(
    [
        Output("adding-rows-table", "data"),
        Output("spot_dropdown", "value", allow_duplicate=True),
    ],
    [
        Input("record_btn", "n_clicks"),
        Input("stored_data", "data"),
        Input("interval_slider", "value"),
        Input("int_std_dropdown", "value"),
        # Input("despike_dropdown", "value"),
    ],
    [
        State("spot_dropdown", "value"),
        State("adding-rows-table", "data"),
        State("adding-rows-table", "columns"),
        State("upload-data", "filename"),
    ],
    prevent_initial_call=True,
)
def add_row(
    n_clicks,
    stored_data,
    interval_slider,
    int_std,
    # despike,
    spot,
    rows,
    columns,
    filename,
):
    if filename == None:
        return rows, spot

    else:
        if spot == None:
            return rows, spot

        else:
            # get information for last button that was clicked in app
            changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

            # if that button was the record button, save all the information from above

            if "record" in changed_id:
                # retrieve data stored in background
                data = pd.read_json(stored_data, orient="split")
                data.set_index("SampleLabel", inplace=True)
                spots = list(data.index.unique())
                current_spot_idx = spots.index(spot)

                # do the lasertram stuff
                current_spot = LaserTRAM(name=spot)
                current_spot.get_data(data.loc[spot, :])
                # if despike == "all":

                #     current_spot.despike_data()

                current_spot.assign_int_std(int_std)
                current_spot.assign_intervals(
                    (interval_slider[0], interval_slider[1]),
                    (interval_slider[2], interval_slider[3]),
                )
                current_spot.get_bkgd_data()
                current_spot.subtract_bkgd()
                current_spot.get_detection_limits()
                current_spot.normalize_interval()
                current_spot.make_output_report()

                row_data = current_spot.output_report.values[0]
                rows.append({c["id"]: r for c, r in zip(columns, row_data)})

                new_spot_idx = current_spot_idx + 1

                if new_spot_idx >= len(spots):
                    new_spot_idx = current_spot_idx

                return rows, spots[new_spot_idx]


# change sample next and previous buttons callback
@app.callback(
    Output("spot_dropdown", "value"),
    [
        Input("skip_btn", "n_clicks"),
        Input("stored_data", "data"),
    ],
    [State("spot_dropdown", "value"), State("upload-data", "filename")],
)
def move_sample(next_clicks, stored_data, spot, filename):
    if filename == None:
        return spot

    else:
        if spot == None:
            return spot

        else:
            changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
            # getting spot list from uploaded data
            data = pd.read_json(stored_data, orient="split")
            data.set_index("SampleLabel", inplace=True)

            spots = list(data.index.unique())
            current_spot_idx = spots.index(spot)

            # moving the spot list one forward or backward based on
            # which button is clicked

            if next_clicks != 0:
                if "skip_btn" in changed_id:
                    new_spot_idx = current_spot_idx + 1

                    if new_spot_idx >= len(spots):
                        new_spot_idx = current_spot_idx

                return spots[new_spot_idx]


# upload data from lasertram output button
@app.callback(
    [
        Output("stored_old_data", "data"),
        Output("int_std_dropdown_reprocess", "options"),
        Output("old_data_table", "columns"),
        Output("old_data_table", "data"),
        Output("int_std_dropdown_reprocess", "value"),
    ],
    Input("upload-data_reprocess", "contents"),
    State("upload-data_reprocess", "filename"),
    State("new_data_table", "columns"),
    State("old_data_table", "columns"),
    State("reprocess_header", "children"),
)

#############################################################################
######################## REPROCESSING TAB ###################################
#############################################################################
def get_oldratio_data(contents, filename, columns, int_std_columns, header):
    # list of standard reference materials currently supported. This can be a
    # fluid list based on what is in the spreadsheet with accepted values

    if filename == None:
        # arbitrary fillers when no data is uploaded
        analytes = [
            {
                "label": "please upload an old LT file",
                "value": "please upload an old LT file",
            }
        ]

        data = pd.DataFrame(np.zeros(len(columns)))
        table_data = pd.DataFrame(np.zeros(len(columns)))
        table_columns = columns.copy()

    elif "xls" in filename:
        # retrieve data from uploaded file. This is the output from the above
        # tabs (either lasertram or lasertram profiler)
        content_type, content_string = contents.split(",")

        decoded = base64.b64decode(content_string)
        # Assume that the user uploaded an excel file
        data = pd.read_excel(io.BytesIO(decoded))
        data["despiked"] = data["despiked"].fillna("None")
        data["omitted_region"] = data["omitted_region"].fillna("None")
        data.dropna(inplace=True)
        cols = data.columns.tolist()

        data = data.set_index(["Spot"])

        analytes = [
            {"label": l, "value": l} for l in data.iloc[:, 9:].columns if "_se" not in l
        ]

        table_data = data.reset_index()
        table_data = table_data.loc[:, cols]
        table_columns = [{"id": str(c), "name": str(c)} for c in table_data.columns]

    return (
        data.to_json(orient="split"),
        analytes,
        table_columns,
        table_data.to_dict("records"),
        analytes[0]["value"],
    )


@app.callback(
    [
        Output("new_data_table", "columns"),
        Output("new_data_table", "data"),
    ],
    Input("stored_old_data", "data"),
    Input("stored_data", "data"),
    Input("int_std_dropdown_reprocess", "options"),
    Input("int_std_dropdown_reprocess", "value"),
    Input("reprocess_btn", "n_clicks"),
)
def reprocess_data(stored_old_df, stored_df, analytes, int_std, n_clicks):
    # dont do anything if the button hasn't been clicked. Need to prevent
    # error from being thrown
    if n_clicks < 1:
        raise exceptions.PreventUpdate

    # once clicked it's go time
    if n_clicks >= 1:
        df = pd.read_json(stored_df, orient="split").set_index("SampleLabel").dropna()
        old_df = pd.read_json(stored_old_df, orient="split").dropna()

        spots_with_data = []
        for spot in df.index.unique().tolist():
            for old_spot in old_df.index.unique().tolist():
                if spot == old_spot:
                    spots_with_data.append(spot)

        df_for_reprocessing = df.loc[spots_with_data, :]

        processed_spots = []

        for spot in spots_with_data:
            # get each spot
            spot_data = df_for_reprocessing.loc[spot, :].copy()

            current_spot = LaserTRAM(name=spot)

            batch.process_spot(
                current_spot,
                raw_data=spot_data.loc[spot, :],
                bkgd=(old_df.loc[spot, "bkgd_start"], old_df.loc[spot, "bkgd_stop"]),
                keep=(old_df.loc[spot, "int_start"], old_df.loc[spot, "int_stop"]),
                int_std=int_std,
                despike=False,
                output_report=True,
            )
            processed_spots.append(current_spot)

        reprocessed_data = pd.DataFrame()
        for spot in processed_spots:
            reprocessed_data = pd.concat([reprocessed_data, spot.output_report])

        return (
            [{"id": str(c), "name": str(c)} for c in reprocessed_data.columns],
            reprocessed_data.to_dict("records"),
        )


#############################################################################
########################### LASERCALC TAB ###################################
#############################################################################


def analyte_to_oxide(int_std):
    """
    return the most likely EPMA oxide for a given internal standard analyte

    Parameters
    ----------
    int_std : string
        the internal standard used from LaserTRAM. This is in the 'norm' column
        of the LaserTRAM output

        currently supported elements:
            'SiO2','TiO2','Al2O3','Cr2O3','MnO','FeO','K2O','CaO','Na2O', 'MgO'

    Returns
    -------
    oxide : string
        the equivalent EPMA oxide for a given internal standard analyte
        e.g. 29Si --> SiO2
             43Ca --> CaO

    """

    el = [i for i in int_std if not i.isdigit()]

    if len(el) == 2:
        element = el[0] + el[1]

    else:
        element = el[0]

    oxides = [
        "SiO2",
        "TiO2",
        "Al2O3",
        "Cr2O3",
        "MnO",
        "FeO",
        "K2O",
        "CaO",
        "Na2O",
        "NiO",
        "MgO",
    ]

    for o in oxides:
        if element in o:
            oxide = o

    return oxide


# upload data from lasertram output button
@app.callback(
    [
        Output("stored_data_c", "data"),
        Output("std_dropdown", "options"),
        Output("int_std_table", "columns"),
        Output("int_std_table", "data"),
        Output("std_dropdown", "value"),
    ],
    Input("upload-data_c", "contents"),
    State("upload-data_c", "filename"),
    State("concentrations_table", "columns"),
    State("int_std_table", "columns"),
    State("table_header", "children"),
)
def get_ratio_data(contents, filename, columns, int_std_columns, header):
    # list of standard reference materials currently supported. This can be a
    # fluid list based on what is in the spreadsheet with accepted values
    pubstandards = [
        "BCR-2G",
        "BHVO-2G",
        "BIR-1G",
        "GSA-1G",
        "GSC-1G",
        "GSD-1G",
        "GSE-1G",
        "NIST-610",
        "NIST-612",
        "NIST-616",
        "BM90201-G",
        "GOR128-G",
        "GOR132-G",
        "ATHO-G",
        "KL2-G",
        "ML3B-G",
        "T1-G",
        "StHs680-G",
    ]

    if filename == None:
        # arbitrary fillers when no data is uploaded
        calib_std_list = [{"label": "Choose calibration std.", "value": "None"}]
        data = pd.DataFrame(np.zeros(len(columns)))
        int_std_data = pd.DataFrame(np.zeros(len(int_std_columns)))

        int_std_table_data = int_std_data.to_dict("records")
        calib_std = None

    elif "xls" in filename:
        # retrieve data from uploaded file. This is the output from the above
        # tabs (either lasertram or lasertram profiler)
        content_type, content_string = contents.split(",")

        decoded = base64.b64decode(content_string)
        # Assume that the user uploaded an excel file
        data = pd.read_excel(io.BytesIO(decoded))
        if "despiked" in data.columns:
            data["despiked"] = data["despiked"].fillna("None")

        else:
            data.insert(2, "despiked", ["None"] * data.shape[0])
        if "omitted_region" in data.columns:
            data["omitted_region"] = data["omitted_region"].fillna("None")
        else:
            data.insert(3, "omitted_region", ["None"] * data.shape[0])

        data.dropna(inplace=True)
        data = data.set_index(["Spot"])

        # data.insert(loc=1, column="index", value=np.arange(1, len(data) + 1))

        spots = list(data.index.unique())

        # Check for potential calibration standards. This will let us know what our options
        # are for choosing calibration standards by looking for spots that have the same string
        # as the standard spreadsheet

        stds_column = [[std for std in pubstandards if std in spot] for spot in spots]

        stds_column = [["unknown"] if not l else l for l in stds_column]

        stds_column = [std for sublist in stds_column for std in sublist]

        # standards that can be used as calibrations standards (must have more than 1 analysis)
        # potential_standards = list(np.unique(stds_column))
        potential_standards = [
            std for std in np.unique(stds_column) if stds_column.count(std) > 1
        ]
        potential_standards.remove("unknown")

        # all of the samples in your input sheet that are NOT potential standards
        all_standards = list(np.unique(stds_column))
        all_standards.remove("unknown")

        # This now denotes whether or not something is a standard
        # or an unknown
        data["sample"] = stds_column

        data.reset_index(inplace=True)
        data.set_index("sample", inplace=True)

        calib_std_list = [{"label": std, "value": std} for std in potential_standards]
        # currently only supports 43Ca or 29Si as calibration standards. Will
        # adjust this soon. DONT FORGET

        int_std_data = pd.DataFrame(
            {
                "Spot": spots,
                "{} wt%".format(analyte_to_oxide(data["norm"].unique()[0])): 10,
                "{} 1stdev%".format(analyte_to_oxide(data["norm"].unique()[0])): 1,
            },
            index=data.index,
        )
        columns = [{"id": c, "name": c} for c in data.columns]
        int_std_columns = [{"id": c, "name": c} for c in int_std_data.columns]

        int_std_table_data = int_std_data.to_dict("records")
        calib_std = potential_standards[0]

    return (
        data.to_json(orient="split"),
        calib_std_list,
        int_std_columns,
        int_std_table_data,
        calib_std,
    )


# upload standard reference material sheet callback
@app.callback(
    [
        Output("stored_stds", "data"),
    ],
    Input("upload-stds", "contents"),
    State("upload-stds", "filename"),
)
def get_stds(contents, filename):
    # This is all for retrieving the standard reference material data
    if filename == None:
        data = pd.DataFrame()

    elif "csv" in filename:
        content_type, content_string = contents.split(",")

        decoded = base64.b64decode(content_string)
        # Assume that the user uploaded a CSV file
        data = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        data.set_index("Standard", inplace=True)

    elif "xls" in filename:
        content_type, content_string = contents.split(",")

        decoded = base64.b64decode(content_string)
        # Assume that the user uploaded an excel file
        data = pd.read_excel(io.BytesIO(decoded))
        # data.set_index("Standard", inplace=True)

    return (data.to_json(orient="split"),)


@app.callback(
    [
        Output("concentrations_table", "data"),
        Output("concentrations_table", "columns"),
        Output("table_header", "children"),
        Output("analyte_dropdown", "options"),
        Output("analyte_dropdown", "value"),
        Output("stored_calibstd_data", "data"),
        Output("calib_std_table", "data"),
        Output("calib_std_table", "columns"),
    ],
    [
        Input("stored_data_c", "data"),
        Input("stored_stds", "data"),
        Input("std_dropdown", "options"),
        Input("std_dropdown", "value"),
        Input("calculate_btn", "n_clicks"),
        Input("int_std_table", "data"),
        Input("drift_alpha", "value"),
        State("table_header", "children"),
    ],
)
# This is the money maker function that does all the heavy lifting.
def calculate_concentrations(
    stored_data,
    stds_data,
    stds,
    calib_std,
    n_clicks,
    table_data,
    alpha,
    header,
):
    # dont do anything if the button hasn't been clicked. Need to prevent
    # error from being thrown
    if n_clicks < 1:
        raise exceptions.PreventUpdate

    # once clicked it's go time
    if n_clicks >= 1:
        # get data and analyte list
        data = pd.read_json(stored_data, orient="split")
        # data.set_index("Spot", inplace=True)
        stds_data = pd.read_json(stds_data, orient="split")

        concentrations = LaserCalc(name="output concentrations")
        concentrations.get_SRM_comps(stds_data)
        concentrations.get_data(data)
        concentrations.set_calibration_standard(calib_std)
        concentrations.drift_check(pval=alpha)
        concentrations.get_calibration_std_ratios()

        table_data_df = pd.DataFrame(table_data)
        table_data_df["sample"] = concentrations.data.index.to_list()
        table_data_df.set_index("sample", inplace=True)

        # get corresponding oxide for internal standard analyte and convert its
        # concentrations from wt% oxide to ppm. Only works with the supported
        # list of oides in the 'analyte_to_oxide' function above.
        oxide = analyte_to_oxide(
            concentrations.calibration_std_data["norm"].unique()[0]
        )

        int_std_oxide_array = pd.to_numeric(
            table_data_df.loc[
                concentrations.samples_nostandards, "{} wt%".format(oxide)
            ]
        ).to_numpy()

        int_std_rel_unc = pd.to_numeric(
            table_data_df.loc[
                concentrations.samples_nostandards, "{} 1stdev%".format(oxide)
            ]
        ).to_numpy()
        concentrations.set_int_std_concentrations(
            spots=concentrations.data.loc["unknown", "Spot"],
            concentrations=int_std_oxide_array,
            uncertainties=int_std_rel_unc,
        )
        concentrations.calculate_concentrations()
        concentrations.get_secondary_standard_accuracies()
    concentrations.calibration_std_stats.index.name = "analyte"
    calib_std_columns = [
        {"id": c, "name": c}
        for c in concentrations.calibration_std_stats.reset_index().columns.tolist()
    ]
    df_all = pd.concat(
        [concentrations.unknown_concentrations, concentrations.SRM_concentrations]
    )
    df_all = df_all.sort_values(by=["timestamp"], ascending=True)

    final_columns = [{"id": c, "name": c} for c in df_all.columns.to_list()]
    header = "Calculated Concentrations: "
    analyte_list = [
        {"label": analyte, "value": analyte} for analyte in concentrations.analytes
    ]
    init_analyte = analyte_list[0]

    return (
        df_all.to_dict("records"),
        final_columns,
        header,
        analyte_list,
        init_analyte,
        concentrations.calibration_std_data.to_json(orient="split"),
        concentrations.calibration_std_stats.reset_index().to_dict("records"),
        calib_std_columns,
    )


@app.callback(
    Output("drift_correct_fig", "figure"),
    [
        Input("analyte_dropdown", "value"),
        Input("stored_calibstd_data", "data"),
        Input("calib_std_table", "data"),
        Input("drift_alpha", "value"),
        Input("calculate_btn", "n_clicks"),
    ],
)
def plot_calib_stds(drift_analyte, calib_std_data, calib_std_stats, alpha, n_clicks):
    if n_clicks < 1:
        raise exceptions.PreventUpdate
    else:
        calib_std_data = pd.read_json(calib_std_data, orient="split")
        calib_std_stats = pd.DataFrame(calib_std_stats).set_index("analyte")
        norm_analyte = calib_std_data["norm"].unique().tolist()[0]
        if isinstance(drift_analyte, dict):
            drift_analyte = drift_analyte["value"]

        x = np.array(
            [np.datetime64(d, "m") for d in calib_std_data["timestamp"]]
        ).astype(np.float64)
        # scatter plot
        drift_fig = px.scatter(
            calib_std_data,
            x=np.cumsum(np.diff(x, prepend=x[0])),
            y=drift_analyte,
            title="Normalized ratios for {} over time".format(
                list(calib_std_data.index.unique())[0]
            ),
        )
        drift_fig.update_traces(
            marker=dict(size=20, color="#8C190D", line=dict(width=2, color="black")),
            selector=dict(mode="markers"),
        )

        # line for the mean value of the calibration standard normalized values
        mean = calib_std_stats.loc[drift_analyte, "mean"]
        drift_fig.add_hline(
            y=mean,
            line_width=3,
            line_dash="dash",
            line_color="green",
            name="observed mean",
        )

        # line for the linear regression through the points
        ypred = (
            calib_std_stats.loc[drift_analyte, "slope"] * x
            + calib_std_stats.loc[drift_analyte, "intercept"]
        )
        drift_fig.add_trace(
            go.Scatter(
                x=np.cumsum(np.diff(x, prepend=x[0])),
                y=ypred,
                mode="lines",
                line=dict(color="black", width=3, dash="dash"),
                name="regression",
            )
        )

        drift_fig.update_layout(
            template="simple_white",
            font=dict(size=20, color=text_color),
            autosize=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        drift_fig.update_yaxes(title_text="{}/{}".format(drift_analyte, norm_analyte))

        drift_fig.update_xaxes(
            title_text="Time in experiment (min)",
            tickcolor=text_color,
            linewidth=2,
            linecolor=text_color,
            row=1,
            col=1,
        )

    return drift_fig


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8049)
