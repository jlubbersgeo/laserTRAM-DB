#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 08:26:36 2021

@author: jordanlubbers
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 13:57:37 2021

@author: jordanlubbers
"""

from dash import dcc, html, Input, Output, State, dash_table, exceptions
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import base64
import io
import re
import statsmodels.api as sm
from statsmodels.tools.eval_measures import rmse
from scipy import stats
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import mendeleev

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
    "backgroundColor": "#119DFF",
    "color": "white",
    "padding": "6px",
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
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
                                        dcc.Store(id="stored_data"),
                                        dbc.Col(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [html.H2("LaserTRAM"),]
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
                                                                                            value="43Ca",
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
                                                                                    dbc.Button(
                                                                                        "Previous",
                                                                                        id="previous_btn",
                                                                                        color="warning",
                                                                                        size="lg",
                                                                                        n_clicks=0,
                                                                                    ),
                                                                                ),
                                                                                dbc.Col(
                                                                                    dbc.Button(
                                                                                        "Next",
                                                                                        id="next_btn",
                                                                                        color="info",
                                                                                        size="lg",
                                                                                        n_clicks=0,
                                                                                    ),
                                                                                ),
                                                                                dbc.Col(
                                                                                    dbc.Button(
                                                                                        "Record",
                                                                                        id="record_btn",
                                                                                        color="success",
                                                                                        size="lg",
                                                                                        n_clicks=0,
                                                                                    ),
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
                                                    color="primary",
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
                                                                                    id="interval_slider",
                                                                                    step=1,
                                                                                    value=[
                                                                                        5,
                                                                                        15,
                                                                                        25,
                                                                                        45,
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
                                                    color="primary",
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
                        )
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
                                        dbc.Col([html.H2("LaserTRAM profiler"),]),
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
                                    color="primary",
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
                                                dcc.Graph(id="raw-data_p",),
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
                                                            [html.H2("LaserCalc"),]
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
                                                                                        0.01
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
                                                    color="primary",
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
                                                                                "overflowX": "auto",
                                                                                "height": 400,
                                                                                "width": "50vh",
                                                                            },
                                                                            fixed_rows={
                                                                                "headers": True
                                                                            },
                                                                            style_cell={
                                                                                # all three widths are needed
                                                                                "minWidth": "20px",
                                                                                "width": "20px",
                                                                                "maxWidth": "20px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
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
                                                        "height": 400,
                                                        "width": "100vh",
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

text_color = "Black"

#%% LaserTRAM callbacks

# upload data callback
@app.callback(
    [
        Output("stored_data", "data"),
        Output("spot_dropdown", "options"),
        Output("adding-rows-table", "columns"),
        Output("int_std_dropdown", "options"),
        Output("int_std_dropdown", "value"),
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

    elif "xls" in filename:
        content_type, content_string = contents.split(",")

        decoded = base64.b64decode(content_string)
        # Assume that the user uploaded an excel file
        data = pd.read_excel(io.BytesIO(decoded))
        data.dropna(inplace=True)

        data = data.set_index(["SampleLabel"])
        
        #######
        if 'timestamp' in [c for c in data.columns]:
            

            # initial columns
            columns = (
                [{"id": "timestamp", "name": "timestamp"}]
                + [{"id": "Spot", "name": "Spot"}]
                + [{"id": "bkgd_start", "name": "bkgd_start"}]
                + [{"id": "bkgd_stop", "name": "bkgd_stop"}]
                + [{"id": "int_start", "name": "int_start"}]
                + [{"id": "int_stop", "name": "int_stop"}]
                + [{"id": "norm", "name": "norm"}]
                + [{"id": "norm_cps", "name": "norm_cps"}]
                + [{"id": c, "name": c} for c in data.iloc[:, 2:].columns]
                + [{"id": c + "_se", "name": c + "_se"} for c in data.iloc[:, 2:].columns]
            )
            
        else:
            # initial columns
            columns = (
                [{"id": "timestamp", "name": "timestamp"}]
                + [{"id": "Spot", "name": "Spot"}]
                + [{"id": "bkgd_start", "name": "bkgd_start"}]
                + [{"id": "bkgd_stop", "name": "bkgd_stop"}]
                + [{"id": "int_start", "name": "int_start"}]
                + [{"id": "int_stop", "name": "int_stop"}]
                + [{"id": "norm", "name": "norm"}]
                + [{"id": "norm_cps", "name": "norm_cps"}]
                + [{"id": c, "name": c} for c in data.iloc[:, 1:].columns]
                + [{"id": c + "_se", "name": c + "_se"} for c in data.iloc[:, 1:].columns]
            )
        ########
            

        spots = list(data.index.unique())
        spot_list = [{"label": spot, "value": spot} for spot in spots]
        analyte_list = [
            {"label": analyte, "value": analyte} for analyte in data.iloc[:, 1:].columns
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

    return data.to_json(orient="split"), spot_list, columns, analyte_list, int_std


# plotting data callback
@app.callback(
    [Output("raw-data", "figure"), Output("error-data", "figure")],
    [
        Input("spot_dropdown", "value"),
        Input("stored_data", "data"),
        Input("interval_slider", "value"),
        Input("int_std_dropdown", "value"),
    ],
    [State("upload-data", "filename")],
)
def plot(spot, stored_data, interval_slider, int_std, filename):
    # empty if nothing is uploaded
    if filename == None:
        fig = {}
        error_fig = {}

        return fig, error_fig

    else:
        # empty if user has not chosen a spot yet
        if spot == None:

            fig = {}
            error_fig = {}

            return fig, error_fig
        else:
            # retrieve data stored in background
            data = pd.read_json(stored_data, orient="split")
            data.set_index("SampleLabel", inplace=True)

            # filter for spot chosen and exclude timestamp column
            if "timestamp" in data.columns.tolist():

                df = data.loc[spot, :]
                df = df.iloc[:, 1:]
            else:

                df = data.loc[spot, :]

            # get time in units of seconds
            df["Time"] = df["Time"] / 1000

            # get analyte list
            elements = df.iloc[:, 1:].columns.tolist()

            # interval positions for background and signal to keep
            bkgd_start_idx = np.where(df["Time"] > interval_slider[0])[0][0]
            bkgd_stop_idx = np.where(df["Time"] > interval_slider[1])[0][0]
            int_start_idx = np.where(df["Time"] > interval_slider[2])[0][0]
            int_stop_idx = np.where(df["Time"] > interval_slider[3])[0][0]

            for e, i in zip(elements, range(len(elements))):
                if e == int_std:
                    break
            int_std_loc = i

            # convert spot data to numpy array
            df_n = df.to_numpy()

            # get median background counts per second for each analyte
            bkgd_data = np.median(df_n[bkgd_start_idx:bkgd_stop_idx, 1:], axis=0)

            # get detection limits for each analyte: 3 std devs from bkgd_data
            detection_limits = (
                np.std(df_n[bkgd_start_idx:bkgd_stop_idx, 1:], axis=0) * 3
            )

            # subtract background from interval signal
            bkgd_correct_data = df_n[int_start_idx:int_stop_idx, 1:] - bkgd_data

            # normalize background corrected data to internal standard data
            bkgd_correct_normal_data = (
                bkgd_correct_data / bkgd_correct_data[:, int_std_loc][:, None]
            )

            # median values for normalized data for interval
            bkgd_correct_med = np.median(bkgd_correct_normal_data, axis=0)

            # flag median values that are below detection limit or 0 with -9999. This flag
            # is used later in laser calc to say they are "b.d.l"
            bkgd_correct_med[
                np.median(bkgd_correct_data, axis=0) <= detection_limits
            ] = -9999
            bkgd_correct_med[np.median(bkgd_correct_data, axis=0) == 0] = -9999

            # standard error of the normalized data over the chosen interval
            se = bkgd_correct_normal_data.std(axis=0) / np.sqrt(
                abs(int_stop_idx - int_start_idx)
            )

            # relative standard error
            rel_se = 100 * (se / bkgd_correct_med)

            # turn numpy array into pandas dataframe and add back in time column.
            # This step makes it easier to plot below
            bkgd_correct_normal_data = pd.DataFrame(
                bkgd_correct_normal_data, columns=elements
            )
            bkgd_correct_normal_data["Time"] = df_n[int_start_idx:int_stop_idx, 0]

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
                y1=df.iloc[:, 1:].max().max(),
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
                y1=df.iloc[:, 1:].max().max(),
                line_width=0,
                fillcolor="red",
                opacity=0.25,
                row=1,
                col=1,
            )
            for i in range(len(elements)):
                fig.add_trace(
                    go.Scatter(
                        x=df["Time"],
                        y=df[elements[i]],
                        mode="lines",
                        name=elements[i],
                        line=dict(color=colorlist[i],),
                    ),
                    row=1,
                    col=1,
                )

                fig.add_trace(
                    go.Scatter(
                        x=bkgd_correct_normal_data["Time"],
                        y=bkgd_correct_normal_data[elements[i]],
                        mode="lines",
                        name=elements[i],
                        showlegend=False,
                        line=dict(color=colorlist[i],),
                    ),
                    row=1,
                    col=2,
                )

            fig.update_layout(
                template="simple_white",
                font=dict(family="Gill Sans", size=18, color=text_color),
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

            err_colors = [
                "gold" if rel_se[x] >= 5 else "green" for x in range(len(rel_se))
            ]

            error_fig = go.Figure(
                go.Bar(
                    x=elements,
                    y=rel_se,
                    marker=dict(color=err_colors),
                    text=bkgd_correct_med,
                    textposition="auto",
                )
            )
            error_fig.update_yaxes(title_text="% SE")
            error_fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
            error_fig.update_layout(
                template="simple_white",
                font=dict(family="Gill Sans", size=18, color=text_color),
                height=300,
                uniformtext_minsize=8,
                uniformtext_mode="hide",
            )

            return fig, error_fig


# add "recorded" data to table for eventual export
@app.callback(
    Output("adding-rows-table", "data"),
    [
        Input("record_btn", "n_clicks"),
        Input("stored_data", "data"),
        Input("spot_dropdown", "value"),
        Input("interval_slider", "value"),
        Input("int_std_dropdown", "value"),
    ],
    [
        State("adding-rows-table", "data"),
        State("adding-rows-table", "columns"),
        State("upload-data", "filename"),
    ],
)
def add_row(
    n_clicks, stored_data, spot, interval_slider, int_std, rows, columns, filename
):
    if filename == None:

        return rows

    else:
        if spot == None:

            return rows

        else:
            # get information for last button that was clicked in app
            changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

            # if that button was the record button, save all the information from above
            if "record_btn" in changed_id:

                data = pd.read_json(stored_data, orient="split")
                data.set_index("SampleLabel", inplace=True)

                # filter for spot chosen and exclude timestamp column
                if "timestamp" in data.columns.tolist():
                    timestamp = str(data.loc[spot, "timestamp"].unique()[0])
                    df = data.loc[spot, :]
                    df = df.iloc[:, 1:]

                else:
                    timestamp = "N/A"
                    df = data.loc[spot, :]

                elements = df.iloc[:, 1:].columns.tolist()

                df["Time"] = df["Time"] / 1000

                bkgd_start_idx = np.where(df["Time"] > interval_slider[0])[0][0]
                bkgd_stop_idx = np.where(df["Time"] > interval_slider[1])[0][0]
                int_start_idx = np.where(df["Time"] > interval_slider[2])[0][0]
                int_stop_idx = np.where(df["Time"] > interval_slider[3])[0][0]

                for e, i in zip(elements, range(len(elements))):
                    if e == int_std:
                        break
                int_std_loc = i

                df_n = df.to_numpy()
                bkgd_data = np.median(df_n[bkgd_start_idx:bkgd_stop_idx, 1:], axis=0)
                detection_limits = (
                    np.std(df_n[bkgd_start_idx:bkgd_stop_idx, 1:], axis=0) * 3
                )
                bkgd_correct_data = df_n[int_start_idx:int_stop_idx, 1:] - bkgd_data
                bkgd_correct_normal_data = (
                    bkgd_correct_data / bkgd_correct_data[:, int_std_loc][:, None]
                )
                bkgd_correct_med = np.median(bkgd_correct_normal_data, axis=0)
                bkgd_correct_med[
                    np.median(bkgd_correct_data, axis=0) <= detection_limits
                ] = -9999
                bkgd_correct_med[np.median(bkgd_correct_data, axis=0) == 0] = -9999
                se = bkgd_correct_normal_data.std(axis=0) / np.sqrt(
                    abs(int_stop_idx - int_start_idx)
                )
                rel_se = 100 * (se / bkgd_correct_med)
                bkgd_correct_normal_data = pd.DataFrame(
                    bkgd_correct_normal_data, columns=elements
                )
                bkgd_correct_normal_data["Time"] = df_n[int_start_idx:int_stop_idx, 0]

                # inserting all the metadata about bkgd and interval
                # start and stop times as well as the int std cps value
                row_data = list(bkgd_correct_med) + list(rel_se)
                row_data.insert(0, spot)

                row_data.insert(1, df["Time"][bkgd_start_idx])
                row_data.insert(2, df["Time"][bkgd_stop_idx])
                row_data.insert(3, df["Time"][int_start_idx])
                row_data.insert(4, df["Time"][int_stop_idx])
                row_data.insert(5, int_std)
                row_data.insert(6, np.median(bkgd_correct_data[int_std_loc]))

                row_data.insert(0, timestamp)

                # NEED TO ADD COLUMN CHANGE TO REFLECT IF THERE IS NOT A TIMESTAMP
                # RIGHT NOW DEFAULT IS IF THERE IS A TIMESTAMP

                rows.append({c["id"]: r for c, r in zip(columns, row_data)})

            return rows


# change sample next and previous buttons callback
@app.callback(
    Output("spot_dropdown", "value"),
    [
        Input("next_btn", "n_clicks"),
        Input("previous_btn", "n_clicks"),
        Input("stored_data", "data"),
    ],
    [State("spot_dropdown", "value"), State("upload-data", "filename")],
)
def move_sample(next_clicks, prev_clicks, stored_data, spot, filename):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

    if filename == None:

        return spot

    else:
        if spot == None:

            return spot

        else:
            # getting spot list from uploaded data
            data = pd.read_json(stored_data, orient="split")
            data.set_index("SampleLabel", inplace=True)

            spots = list(data.index.unique())
            current_spot_idx = spots.index(spot)

            # moving the spot list one forward or backward based on
            # which button is clicked

            if next_clicks != 0 or prev_clicks != 0:

                if "next_btn" in changed_id:

                    new_spot_idx = current_spot_idx + 1

                    if new_spot_idx >= len(spots):

                        new_spot_idx = current_spot_idx

                if "previous_btn" in changed_id:
                    new_spot_idx = current_spot_idx - 1

                    if new_spot_idx == 0:

                        new_spot_idx = 1

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
        data.dropna(inplace=True)
        cols = data.columns.tolist()

        data = data.set_index(["Spot"])
        if "timestamp" in data.columns.tolist():

            analytes = [
                {"label": l, "value": l}
                for l in data.iloc[:, 8:].columns
                if "_se" not in l
            ]

        else:
            analytes = [
                {"label": l, "value": l}
                for l in data.iloc[:, 7:].columns
                if "_se" not in l
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
    [Output("new_data_table", "columns"), Output("new_data_table", "data"),],
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
        if "timestamp" in df_for_reprocessing.columns.tolist():

            elements = df_for_reprocessing.iloc[:, 2:].columns.tolist()

        else:

            elements = df_for_reprocessing.iloc[:, 1:].columns.tolist()

        medians = []
        rel_ses = []
        norm_counts = []
        timestamps = []
        for spot in spots_with_data:

            # get each spot
            spot_data = df_for_reprocessing.loc[spot, :].copy()
            # get time in seconds
            spot_data.loc[:, "Time"] = spot_data["Time"] / 1000

            # get bkgd and interval times from old experiment data
            bkgd_start_idx = np.where(
                spot_data["Time"] > old_df.loc[spot, "bkgd_start"]
            )[0][0]
            bkgd_stop_idx = np.where(spot_data["Time"] > old_df.loc[spot, "bkgd_stop"])[
                0
            ][0]
            int_start_idx = np.where(spot_data["Time"] > old_df.loc[spot, "int_start"])[
                0
            ][0]
            int_stop_idx = np.where(spot_data["Time"] > old_df.loc[spot, "int_stop"])[
                0
            ][0]

            # make numpy array, this is all the same as the actual lasertram
            if "timestamp" in spot_data.columns.tolist():

                timestamp = str(spot_data["timestamp"].unique()[0])
                df_n = spot_data.iloc[:, 1:].to_numpy()

            else:
                timestamp = "N/A"
                df_n = spot_data.to_numpy()

            int_std_loc = [elements.index(i) for i in elements if int_std in i][0]
            
           
            # get median background counts per second for each analyte
            bkgd_data = np.median(df_n[bkgd_start_idx:bkgd_stop_idx, 1:], axis=0)

            # get detection limits for each analyte: 3 std devs from bkgd_data
            detection_limits = (
                np.std(df_n[bkgd_start_idx:bkgd_stop_idx, 1:], axis=0) * 3
            )

            # subtract background from interval signal
            bkgd_correct_data = df_n[int_start_idx:int_stop_idx, 1:] - bkgd_data

            # normalize background corrected data to internal standard data
            bkgd_correct_normal_data = (
                bkgd_correct_data / bkgd_correct_data[:, int_std_loc][:, None]
            )

            # median values for normalized data for interval
            bkgd_correct_med = np.median(bkgd_correct_normal_data, axis=0)

            # flag median values that are below detection limit or 0 with -9999. This flag
            # is used later in laser calc to say they are "b.d.l"
            bkgd_correct_med[
                np.median(bkgd_correct_data, axis=0) <= detection_limits
            ] = -9999
            bkgd_correct_med[np.median(bkgd_correct_data, axis=0) == 0] = -9999

            # standard error of the normalized data over the chosen interval
            se = bkgd_correct_normal_data.std(axis=0) / np.sqrt(
                abs(int_stop_idx - int_start_idx)
            )

            # relative standard error
            rel_se = 100 * (se / bkgd_correct_med)

            
            norm_counts.append(np.median(bkgd_correct_data[:, int_std_loc]))
            medians.append(bkgd_correct_med)
            rel_ses.append(rel_se)
            timestamps.append(timestamp)
            
           

        medians_df = pd.DataFrame(medians, columns=elements)
        rel_se_df = pd.DataFrame(
            rel_ses, columns=["{}_se".format(element) for element in elements]
        )

        reprocessed_data = pd.concat(
            [
                old_df.loc[
                    spots_with_data,
                    ["bkgd_start", "bkgd_stop", "int_start", "int_stop"],
                ]
                .reset_index()
                .drop("index", axis="columns"),
                medians_df,
                rel_se_df,
            ],
            axis="columns",
        )

        reprocessed_data.insert(0, "timestamp", timestamps)
        reprocessed_data.insert(1, "Spot", spots_with_data)

        reprocessed_data.insert(6, "norm", int_std)
        reprocessed_data.insert(7, "norm_cps", norm_counts)

        return (
            [{"id": str(c), "name": str(c)} for c in reprocessed_data.columns],
            reprocessed_data.to_dict("records"),
        )


#%%
# LaserTRAM profiler
# This is relatively uncommented because it is functionally the same as
# the LaserTRAM tab functions above. Where different it will be commented.

# upload data callback
@app.callback(
    [
        Output("stored_data_p", "data"),
        Output("adding-rows-table_p", "columns"),
        Output("int_std_dropdown_p", "options"),
        Output("int_std_dropdown_p", "value"),
        Output("interval_slider_p", "max"),
    ],
    Input("upload-data_p", "contents"),
    State("upload-data_p", "filename"),
)
def get_profile_data(contents, filename):
    if filename == None:
        data = pd.DataFrame()
        columns = [
            {"id": "analyte-{}".format(i), "name": "analyte-{}".format(i)}
            for i in range(1, 5)
        ]
        analyte_list = [{"label": "Choose analyte", "value": "None"}]
        int_std = "None"
        slider_max = 100

    elif "csv" in filename:
        content_type, content_string = contents.split(",")

        decoded = base64.b64decode(content_string)
        # Assume that the user uploaded an excel file
        data = pd.read_csv(io.BytesIO(decoded))
        data.dropna(inplace=True)
        columns = (
            [{"id": "Spot", "name": "Spot"}]
            + [{"id": "bkgd_start", "name": "bkgd_start"}]
            + [{"id": "bkgd_stop", "name": "bkgd_stop"}]
            + [{"id": "int_start", "name": "int_start"}]
            + [{"id": "int_stop", "name": "int_stop"}]
            + [{"id": "norm", "name": "norm"}]
            + [{"id": "norm_cps", "name": "norm_cps"}]
            + [{"id": c, "name": c} for c in data.iloc[:, 1:].columns]
            + [{"id": c + "_se", "name": c + "_se"} for c in data.iloc[:, 1:].columns]
        )

        analyte_list = [
            {"label": analyte, "value": analyte} for analyte in data.iloc[:, 1:].columns
        ]

        if "43Ca" in data.iloc[:, 1:].columns:
            int_std = "43Ca"

        elif "43Ca" not in data.iloc[:, 1:].columns:
            if "29Si" in data.iloc[:, 1:].columns:
                int_std = "29Si"
        else:
            int_std = list(data.iloc[:, 1:].columns)[0]

        slider_max = int(data["Time"].max())

    return data.to_json(orient="split"), columns, analyte_list, int_std, slider_max


# ----------------------

# plotting profile callback
@app.callback(
    [Output("raw-data_p", "figure"), Output("error-data_p", "figure")],
    [
        Input("stored_data_p", "data"),
        Input("interval_slider_p", "value"),
        Input("int_std_dropdown_p", "value"),
    ],
    [State("upload-data_p", "filename")],
)
def plot_profile(stored_data, interval_slider, int_std, filename):

    if filename == None:

        fig = {}
        error_fig = {}

        return fig, error_fig

    else:
        # get data from stored data. No need to filter for spots here
        df = pd.read_json(stored_data, orient="split")
        df.dropna(inplace=True)

        elements = df.iloc[:, 1:].columns.tolist()
        bkgd_start_idx = np.where(df["Time"] > interval_slider[0])[0][0]
        bkgd_stop_idx = np.where(df["Time"] > interval_slider[1])[0][0]
        int_start_idx = np.where(df["Time"] > interval_slider[2])[0][0]
        int_stop_idx = np.where(df["Time"] > interval_slider[3])[0][0]

        for e, i in zip(elements, range(len(elements))):
            if e == int_std:
                break
        int_std_loc = i

        df_n = df.to_numpy()
        # int_std_loc = [elements.index(i) for i in elements if int_std in i]
        bkgd_data = np.median(df_n[bkgd_start_idx:bkgd_stop_idx, 1:], axis=0)
        detection_limits = np.std(df_n[bkgd_start_idx:bkgd_stop_idx, 1:], axis=0) * 3
        bkgd_correct_data = df_n[int_start_idx:int_stop_idx, 1:] - bkgd_data
        bkgd_correct_normal_data = (
            bkgd_correct_data / bkgd_correct_data[:, int_std_loc][:, None]
        )
        bkgd_correct_med = np.median(bkgd_correct_normal_data, axis=0)
        bkgd_correct_med[
            np.median(bkgd_correct_data, axis=0) <= detection_limits
        ] = -9999
        bkgd_correct_med[np.median(bkgd_correct_data, axis=0) == 0] = -9999
        se = bkgd_correct_normal_data.std(axis=0) / np.sqrt(
            abs(int_stop_idx - int_start_idx)
        )
        rel_se = 100 * (se / bkgd_correct_med)
        bkgd_correct_normal_data = pd.DataFrame(
            bkgd_correct_normal_data, columns=elements
        )
        bkgd_correct_normal_data["Time"] = df_n[int_start_idx:int_stop_idx, 0]

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
            y1=df.iloc[:, 1:].max().max(),
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
            y1=df.iloc[:, 1:].max().max(),
            line_width=0,
            fillcolor="red",
            opacity=0.25,
            row=1,
            col=1,
        )
        for i in range(len(elements)):
            fig.add_trace(
                go.Scatter(
                    x=df["Time"],
                    y=df[elements[i]],
                    mode="lines",
                    name=elements[i],
                    line=dict(color=colorlist[i],),
                ),
                row=1,
                col=1,
            )

            fig.add_trace(
                go.Scatter(
                    x=bkgd_correct_normal_data["Time"],
                    y=bkgd_correct_normal_data[elements[i]],
                    mode="lines",
                    name=elements[i],
                    showlegend=False,
                    line=dict(color=colorlist[i],),
                ),
                row=1,
                col=2,
            )
        fig.update_layout(
            template="simple_white",
            font=dict(family="Gill Sans", size=18, color=text_color),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            autosize=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title_text="Profile: {}".format(filename.replace(".csv", "")),
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

        err_colors = ["gold" if rel_se[x] >= 5 else "green" for x in range(len(rel_se))]

        error_fig = go.Figure(
            go.Bar(
                x=elements,
                y=rel_se,
                marker=dict(color=err_colors),
                text=bkgd_correct_med,
                textposition="auto",
            )
        )
        error_fig.update_yaxes(title_text="% SE")
        error_fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
        error_fig.update_layout(
            template="simple_white",
            font=dict(family="Gill Sans", size=18, color=text_color),
            height=300,
            uniformtext_minsize=8,
            uniformtext_mode="hide",
        )

        return fig, error_fig


# add data to table after record button is pressed
# --------------
@app.callback(
    Output("adding-rows-table_p", "data"),
    [
        Input("record_btn_p", "n_clicks"),
        Input("stored_data_p", "data"),
        Input("interval_slider_p", "value"),
        Input("int_std_dropdown_p", "value"),
    ],
    [
        State("adding-rows-table_p", "data"),
        State("adding-rows-table_p", "columns"),
        State("upload-data_p", "filename"),
    ],
)
def add_row_p(n_clicks, stored_data, interval_slider, int_std, rows, columns, filename):
    if filename == None:

        return rows

    else:
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

        if "record_btn" in changed_id:

            df = pd.read_json(stored_data, orient="split")
            elements = df.iloc[:, 1:].columns.tolist()

            spot = n_clicks
            bkgd_start_idx = np.where(df["Time"] > interval_slider[0])[0][0]
            bkgd_stop_idx = np.where(df["Time"] > interval_slider[1])[0][0]
            int_start_idx = np.where(df["Time"] > interval_slider[2])[0][0]
            int_stop_idx = np.where(df["Time"] > interval_slider[3])[0][0]

            for e, i in zip(elements, range(len(elements))):
                if e == int_std:
                    break
            int_std_loc = i

            df_n = df.to_numpy()
            bkgd_data = np.median(df_n[bkgd_start_idx:bkgd_stop_idx, 1:], axis=0)
            detection_limits = (
                np.std(df_n[bkgd_start_idx:bkgd_stop_idx, 1:], axis=0) * 3
            )
            bkgd_correct_data = df_n[int_start_idx:int_stop_idx, 1:] - bkgd_data
            bkgd_correct_normal_data = (
                bkgd_correct_data / bkgd_correct_data[:, int_std_loc][:, None]
            )
            bkgd_correct_med = np.median(bkgd_correct_normal_data, axis=0)
            bkgd_correct_med[
                np.median(bkgd_correct_data, axis=0) <= detection_limits
            ] = -9999
            bkgd_correct_med[np.median(bkgd_correct_data, axis=0) == 0] = -9999
            se = bkgd_correct_normal_data.std(axis=0) / np.sqrt(
                abs(int_stop_idx - int_start_idx)
            )
            rel_se = 100 * (se / bkgd_correct_med)
            bkgd_correct_normal_data = pd.DataFrame(
                bkgd_correct_normal_data, columns=elements
            )
            bkgd_correct_normal_data["Time"] = df_n[int_start_idx:int_stop_idx, 0]

            row_data = list(bkgd_correct_med) + list(rel_se)
            row_data.insert(0, "{}_spot_{}".format(filename.replace(".csv", ""), spot))
            row_data.insert(1, df["Time"][bkgd_start_idx])
            row_data.insert(2, df["Time"][bkgd_stop_idx])
            row_data.insert(3, df["Time"][int_start_idx])
            row_data.insert(4, df["Time"][int_stop_idx])
            row_data.insert(5, int_std)
            row_data.insert(6, np.median(bkgd_correct_data[int_std_loc]))

            rows.append({c["id"]: r for c, r in zip(columns, row_data)})

        return rows


# jump interval based on input value and button clicks callback
# ----------
@app.callback(
    Output("interval_slider_p", "value"),
    [
        Input("forward_btn_p", "n_clicks"),
        Input("back_btn_p", "n_clicks"),
        Input("step_val_p", "value"),
    ],
    [State("upload-data_p", "filename"), State("interval_slider_p", "value")],
)
def jump(n_clicks_f, n_clicks_b, step_val, filename, interval_slider):
    if filename == None:

        return interval_slider

    else:
        # this jumps the interval by the amount specified in the step_val input
        # box. Checks to see which button was clicked and then acts accordingly
        # e.g. moving the interval forward or backwards
        if n_clicks_f != 0 or n_clicks_b != 0:

            changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

            if "forward_btn" in changed_id:

                interval_slider[0] = interval_slider[0]
                interval_slider[1] = interval_slider[1]
                interval_slider[2] = interval_slider[2] + step_val
                interval_slider[3] = interval_slider[3] + step_val

            elif "back_btn" in changed_id:

                interval_slider[0] = interval_slider[0]
                interval_slider[1] = interval_slider[1]
                interval_slider[2] = interval_slider[2] - step_val
                interval_slider[3] = interval_slider[3] - step_val

        return interval_slider


#%%
# these two functions are for converting oxide concentrations of internal std
# to ppm.


def analyte_to_oxide(int_std):
    """
    return the most likely EPMA oxide for a given internal standard analyte

    Parameters
    ----------
    int_std : string
        the internal standard used from LaserTRAM. This is in the 'norm' column
        of the LaserTRAM output
        
        currently supported elements:
            'SiO2','TiO2','Al2O3','Cr2O3','MnO','FeO','K2O','CaO','Na2O'

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
    ]

    for o in oxides:

        if element in o:

            oxide = o

    return oxide


def oxide_to_ppm(wt_percent, int_std):
    """
    convert concentration internal standard analyte oxide in weight percent to 
    concentration ppm for a 1D series of data

    Parameters
    ----------
    wt_percent : array-like
        the oxide values to be converted to ppm
    int_std : string
        the internal standard used in the experiment (e.g., '29Si', '43Ca', 
                                                      '47Ti')
        currently supported elements:
            
            'SiO2','TiO2','Al2O3','Cr2O3','MnO','FeO','K2O','CaO','Na2O'

    Returns
    -------
    ppm : array-like
        concentrations in ppm the same shape as the wt_percent input

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
    ]

    for o in oxides:

        if element in o:

            oxide = o

    s = oxide.split("O")
    cat_subscript = s[0]
    an_subscript = s[1]

    cat_subscript = [i for i in cat_subscript if i.isdigit()]
    if cat_subscript:
        cat_subscript = int(cat_subscript[0])
    else:
        cat_subscript = 1

    an_subscript = [i for i in an_subscript if i.isdigit()]
    if an_subscript:
        an_subscript = int(an_subscript[0])
    else:
        an_subscript = 1

    ppm = 1e4 * (
        (wt_percent * mendeleev.element(element).atomic_weight * cat_subscript)
        / (
            mendeleev.element(element).atomic_weight
            + mendeleev.element("O").atomic_weight * an_subscript
        )
    )
    return ppm


# LaserCalc
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
        data.dropna(inplace=True)
        data = data.set_index(["Spot"])

        data.insert(loc=1, column="index", value=np.arange(1, len(data) + 1))

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
    [Output("stored_stds", "data"),],
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
        data.set_index("Standard", inplace=True)

    return (data.to_json(orient="split"),)


# calculate concentrations based on uploaded data and chosen calibration
# standard from dropdown
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
    stored_data, stds_data, stds, calib_std, n_clicks, table_data, alpha, header,
):
    # dont do anything if the button hasn't been clicked. Need to prevent
    # error from being thrown
    if n_clicks < 1:
        raise exceptions.PreventUpdate

    # once clicked it's go time
    if n_clicks >= 1:
        # get data and analyte list
        data = pd.read_json(stored_data, orient="split")
        data.set_index("Spot", inplace=True)

        myanalytes = [
            analyte
            for analyte in data.columns.tolist()
            if not (
                "_se" in analyte
                or "norm" in analyte
                or "index" in analyte
                or "Spot" in analyte
                or "wt%" in analyte
                or "1stdev%" in analyte
                or "start" in analyte
                or "stop" in analyte
                or "long" in analyte
                or "timestamp" in analyte
            )
        ]

        analyte_list = [{"label": analyte, "value": analyte} for analyte in myanalytes]

        # myanalytes.remove(data['norm'].unique()[0])

        spots = list(data.index.unique())

        # Get a list of all of the elements supported in the published standard datasheet
        # Get a second list for the same elements but their corresponding uncertainty columns
        stds_data = pd.read_json(stds_data, orient="split")

        standard_elements = [
            analyte for analyte in stds_data.columns.tolist() if not ("_std" in analyte)
        ]

        # list of standards in uploaded spreadsheet
        pubstandards = stds_data.index.unique().tolist()

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

        table_data_df = pd.DataFrame(table_data)
        table_data_df["sample"] = stds_column
        table_data_df.set_index("sample", inplace=True)

        # list of columns that pertain to analyte uncertainties
        myuncertainties = [analyte + "_se" for analyte in myanalytes]

        # create a separate dataframe for our calibration standard data
        calib_std_data = data.loc[calib_std, :]

        # Calibration standard information
        # mean
        calib_std_means = calib_std_data.loc[:, myanalytes + myuncertainties].mean()
        # std deviation
        calib_std_stds = calib_std_data.loc[:, myanalytes + myuncertainties].std()
        # relative standard error
        calib_std_ses = 100 * (
            (calib_std_stds / calib_std_means) / np.sqrt(calib_std_data.shape[0])
        )

        calib_std_rmses = []
        calib_std_slopes = []
        calib_std_intercepts = []
        drift_check = []

        # For our calibration standard, calculate the concentration ratio of each
        # analyte to the element used as the internal standard
        std_conc_ratios = []
        myanalytes_nomass = []
        # go through each analyte and check to see whether or not it needs to be
        # drift corrected. This is outlined in the documentation for the criteria
        # If regression has significant p val and F stat, correct. Else just take mean of
        # calibration standard data
        for j in range(len(myanalytes)):

            # Getting regression statistics on analyte normalized ratios through time
            # for the calibration standard. This is what we use to check to see if it needs
            # to be drift corrected
            if "timestamp" in calib_std_data.columns.tolist():
                # get an array in time units based on timestamp column. This is
                # is in seconds
                x = np.array(
                    [np.datetime64(d, "m") for d in calib_std_data["timestamp"]]
                ).astype(np.float64)

            else:
                #uses the analysis number if there is not a timestamp column
                x = calib_std_data["index"]

            y = calib_std_data[myanalytes[j]]

            X = sm.add_constant(x)
            # Note the difference in argument order
            model = sm.OLS(y, X).fit()
            # now generate predictions
            ypred = model.predict(X)

            # calc rmse
            RMSE = rmse(y, ypred)
            
            if model.params.shape[0] < 2:
               calib_std_slopes.append(model.params[0])
               calib_std_intercepts.append(0)
               
            else:
               
               calib_std_slopes.append(model.params[1])
               calib_std_intercepts.append(model.params[0])

            calib_std_rmses.append(RMSE)
            # calib_std_slopes.append(model.params[1])
            # calib_std_intercepts.append(model.params[0])

            # f value stuff
            fvalue = model.fvalue
            f_pvalue = model.f_pvalue
            # alpha is our confidence value. Default would be 99% so it has
            # to be very linear to drift correct
            fcrit = stats.f.ppf(q=1 - alpha, dfn=len(x) - 1, dfd=len(y) - 1)

            if (f_pvalue < alpha) and (fvalue > fcrit):
                drift = "True"
                drift_check.append(drift)
            else:
                drift = "False"
                drift_check.append(drift)


        for i in range(len(myanalytes)):
            # strip the atomic number from our analyte data
            nomass = re.split("(\d+)", myanalytes[i])[2]
            # make it a list
            myanalytes_nomass.append(nomass)

            # if our element is in the list of standard elements take the ratio
            if nomass in standard_elements:
                std_conc_ratios.append(
                    stds_data.loc[calib_std, nomass]
                    / stds_data.loc[
                        calib_std,
                        re.split("(\d+)", calib_std_data["norm"].unique()[0])[2],
                    ]
                )

        # make our list an array for easier math going forward
        # std_conc_ratios = pd.DataFrame(np.array(std_conc_ratios)[np.newaxis,:],columns = myanalytes)
        std_conc_ratios = np.array(std_conc_ratios)

    # all of the samples in your input sheet that are NOT potential calibration standards
    samples_nostandards = list(np.setdiff1d(stds_column, all_standards))

    # get corresponding oxide for internal standard analyte and convert its
    # concentrations from wt% oxide to ppm. Only works with the supported
    # list of oides in the 'analyte_to_oxide' function above.
    oxide = analyte_to_oxide(calib_std_data["norm"].unique()[0])

    int_std_oxide_array = pd.to_numeric(
        table_data_df.loc[samples_nostandards, "{} wt%".format(oxide)]
    ).to_numpy()

    int_std_concentration = oxide_to_ppm(
        int_std_oxide_array, calib_std_data["norm"].unique()[0]
    )

    unknown_int_std_unc = pd.to_numeric(
        table_data_df.loc[samples_nostandards, "{} 1stdev%".format(oxide)]
    ).to_numpy()


    # iterate through list of all standards in dataset that have data in the 
    # laicpms_stds_tidy.xlsx sheet
    secondary_standards = all_standards.copy()
    secondary_standards.remove(calib_std)
    concentrations_list = []

    for standard in secondary_standards:
        drift_concentrations_list = []

        for j, analyte, slope, intercept, drift in zip(
            range(len(myanalytes)),
            myanalytes,
            calib_std_slopes,
            calib_std_intercepts,
            drift_check,
        ):
            #working with analytes that have been drift corrected
            if "True" in drift:
                if "timestamp" in data.columns.tolist():
                    # if there is timestamp data use that to get the normalized
                    #ratio of the analyte in the calibration standard rather 
                    # than the mean
                    frac = (
                        slope
                        * np.array(
                            [
                                np.datetime64(d, "m")
                                for d in data.loc[standard, "timestamp"]
                            ]
                        ).astype(np.float64)
                        + intercept
                    )
                    
                else:
                    #if there is no timestamp info just do the same as above with 
                    # the analysis number as the x var
                    frac = slope * data.loc[standard, "index"] + intercept
                    
                    
                # concentration of analyte that has been drift corrected
                drift_concentrations = (
                    (
                        stds_data.loc[
                            standard,
                            re.split("(\d+)", calib_std_data["norm"].unique()[0])[2],
                        ]
                    )
                    * (std_conc_ratios[j] / frac)
                    * data.loc[standard, analyte]
                )
                
                # take care of potential standards that have only one analysis
                # i.e. a 1D array. This forces things to be in the right shape 
                # to be in a pandas dataframe later
                if type(drift_concentrations) == np.float64:
                    df = pd.DataFrame(
                        np.array([drift_concentrations]), columns=[analyte]
                    )

                else:
                    df = pd.DataFrame(drift_concentrations, columns=[analyte])

                drift_concentrations_list.append(df)

        # if there are more than one secondary standard combine the individual
        # dataframes into one
        if len(drift_concentrations_list) > 0:

            drift_df = pd.concat(drift_concentrations_list, axis="columns")
            #takes care of one analysis standards so they are compatible with
            # standards that are more than one analysis
            if drift_df.shape[0] == 1:
                drift_df["sample"] = standard
                drift_df.set_index("sample", inplace=True)
                
            #calculate concentrations
            concentrations = (
                (
                    stds_data.loc[
                        standard,
                        re.split("(\d+)", calib_std_data["norm"].unique()[0])[2],
                    ]
                )
                * (std_conc_ratios / calib_std_means[myanalytes])
                * data.loc[standard, myanalytes]
            )
            
            # Replace analyte values with drift corrected
            # value
            for column in drift_df.columns.tolist():
                #this situation should rarely be encountered but takes care of 
                # 1 analysis standards
                if type(concentrations) == pd.Series:
                    concentrations.loc[column] = drift_df[column].to_numpy()[0]

                else:
                    #multiple analysis standards
                    concentrations[column] = drift_df[column]
                    
                    
            # If 1 analysis standard force into correct shape for concating 
            # later
            if type(concentrations) == pd.Series:
                concentrations = pd.DataFrame(concentrations).T
                concentrations["sample"] = standard
                concentrations.set_index("sample", inplace=True)

            concentrations_list.append(concentrations)
            
            
            
        else:
            concentrations = (
                (
                    stds_data.loc[
                        standard,
                        re.split("(\d+)", calib_std_data["norm"].unique()[0])[2],
                    ]
                )
                * (std_conc_ratios / calib_std_means[myanalytes])
                * data.loc[standard, myanalytes]
            )
            concentrations_list.append(concentrations)

    # Below calculates the concentrations of all unknown analyses using the same 
    # logic as above with the standards, it just does not search the uploaded standards
    # data for internal standards concentration. This is instead input by the user

    unknown_concentrations_list = []
    # creates a list of dataframes, one for each sample, that holds the concentration information

    for sample in samples_nostandards:

        drift_concentrations_list = []

        for j, analyte, slope, intercept, drift in zip(
            range(len(myanalytes)),
            myanalytes,
            calib_std_slopes,
            calib_std_intercepts,
            drift_check,
        ):

            if "True" in drift:
                if "timestamp" in data.columns.tolist():
                    frac = (
                        slope
                        * np.array(
                            [
                                np.datetime64(d, "m")
                                for d in data.loc[sample, "timestamp"]
                            ]
                        ).astype(np.float64)
                        + intercept
                    )
                else:

                    frac = data.loc[sample, "index"] + intercept

                drift_concentrations = (
                    data.loc[sample, analyte]
                    * (std_conc_ratios[j] / frac)
                    * (int_std_concentration)
                )

                if type(drift_concentrations) == np.float64:
                    df = pd.DataFrame(
                        np.array([drift_concentrations]), columns=[analyte]
                    )

                else:
                    df = pd.DataFrame(drift_concentrations, columns=[analyte])

                drift_concentrations_list.append(df)

        if len(drift_concentrations_list) > 0:

            drift_df = pd.concat(drift_concentrations_list, axis="columns")
            if drift_df.shape[0] == 1:
                drift_df["sample"] = standard
                drift_df.set_index("sample", inplace=True)

            unknown_concentrations = (
                data.loc[sample, myanalytes]
                * (std_conc_ratios / calib_std_means[myanalytes])
                * (int_std_concentration[:, np.newaxis])
            )

            for column in drift_df.columns.tolist():
                if type(unknown_concentrations) == pd.Series:
                    unknown_concentrations.loc[column] = drift_df[column].to_numpy()[0]

                else:
                    unknown_concentrations[column] = drift_df[column]

            if type(unknown_concentrations) == pd.Series:
                unknown_concentrations = pd.DataFrame(concentrations).T
                unknown_concentrations["sample"] = sample
                unknown_concentrations.set_index("sample", inplace=True)
    
            unknown_concentrations_list.append(unknown_concentrations)
        else:
            unknown_concentrations = (
                data.loc[sample, myanalytes]
                * (std_conc_ratios / calib_std_means[myanalytes])
                * (int_std_concentration[:, np.newaxis])
            )

            unknown_concentrations_list.append(unknown_concentrations)

    # Incorporating uncertainty in the calibration standard
    calib_uncertainty = True
    stds_list = []
    unknowns_list = []

    # use RMSE of regression for elements where drift correction is applied rather than the standard error
    # of the mean of all the calibration standard normalized ratios

    for j in range(len(drift_check)):
        if "True" in drift_check[j]:
            calib_std_means[j] = 100 * calib_std_rmses[j] / calib_std_means[j]

    # creates a list of dataframes that hold the uncertainty information for each secondary standard.
    for standard, concentration in zip(secondary_standards, concentrations_list):

        # concentration of internal standard in unknown uncertainties
        t1 = (
            stds_data.loc[
                standard,
                "{}_std".format(
                    re.split("(\d+)", calib_std_data["norm"].unique()[0])[2]
                ),
            ]
            / stds_data.loc[
                standard,
                "{}".format(re.split("(\d+)", calib_std_data["norm"].unique()[0])[2]),
            ]
        ) ** 2

        # concentration of internal standard in calibration standard uncertainties
        t2 = (
            stds_data.loc[
                calib_std,
                "{}_std".format(
                    re.split("(\d+)", calib_std_data["norm"].unique()[0])[2]
                ),
            ]
            / stds_data.loc[
                calib_std,
                "{}".format(re.split("(\d+)", calib_std_data["norm"].unique()[0])[2]),
            ]
        ) ** 2

        # concentration of each analyte in calibration standard uncertainties
        std_conc_stds = []
        for i in range(len(myanalytes)):
            # strip the atomic number from our analyte data
            nomass = re.split("(\d+)", myanalytes[i])[2]

            # if our element is in the list of standard elements take the ratio
            if nomass in standard_elements:
                std_conc_stds.append(
                    (
                        stds_data.loc[calib_std, "{}_std".format(nomass)]
                        / stds_data.loc[calib_std, nomass]
                    )
                    ** 2
                )

        std_conc_stds = np.array(std_conc_stds)

        # Overall uncertainties

        if calib_uncertainty == True:
            stds_values = concentration * np.sqrt(
                np.array(
                    t1
                    + t2
                    + std_conc_stds
                    + (calib_std_ses[myanalytes].to_numpy()[np.newaxis, :] / 100) ** 2
                    + (data.loc[standard, myuncertainties].to_numpy() / 100)** 2
                ).astype(np.float64)
            )
            stds_values.columns = myuncertainties
            stds_list.append(stds_values)
        else:
            stds_values = concentration * np.sqrt(
                t2
                + std_conc_stds
                + (calib_std_ses[myanalytes].to_numpy()[np.newaxis, :] / 100) ** 2
                + (data.loc[standard, myuncertainties].to_numpy() / 100) ** 2
            )
            stds_values.columns = myuncertainties
            stds_list.append(stds_values)

    # creates a list of dataframes that hold the uncertainty information for unknown spot.
    for sample, concentration in zip(samples_nostandards, unknown_concentrations_list):

        # concentration of internal standard in unknown uncertainties
        t1 = (unknown_int_std_unc / 100) ** 2

        # concentration of internal standard in calibration standard uncertainties
        t2 = (
            stds_data.loc[
                calib_std,
                "{}_std".format(
                    re.split("(\d+)", calib_std_data["norm"].unique()[0])[2]
                ),
            ]
            / stds_data.loc[
                calib_std,
                "{}".format(re.split("(\d+)", calib_std_data["norm"].unique()[0])[2]),
            ]
        ) ** 2

        # concentration of each analyte in calibration standard uncertainties
        std_conc_stds = []
        for i in range(len(myanalytes)):
            # strip the atomic number from our analyte data
            nomass = re.split("(\d+)", myanalytes[i])[2]

            # if our element is in the list of standard elements take the ratio
            if nomass in standard_elements:
                std_conc_stds.append(
                    (
                        stds_data.loc[calib_std, "{}_std".format(nomass)]
                        / stds_data.loc[calib_std, nomass]
                    )
                    ** 2
                )

        std_conc_stds = np.array(std_conc_stds)
        # incorporate uncertainty in calibration standard
        if calib_uncertainty == True:
            unknown_stds_values = concentration * np.sqrt(
                t1[:, np.newaxis]
                + t2
                + std_conc_stds
                + (calib_std_ses[myanalytes].to_numpy()[np.newaxis, :] / 100) ** 2
                +  (data.loc[sample, myuncertainties].to_numpy() / 100)** 2
            )
            unknown_stds_values.columns = myuncertainties
            unknowns_list.append(unknown_stds_values)
        else:
            unknown_stds_values = concentration * np.sqrt(
                t2
                + std_conc_stds
                + (calib_std_ses[myanalytes].to_numpy()[np.newaxis, :] / 100) ** 2
                + (data.loc[sample, myuncertainties].to_numpy() / 100)** 2
            )
            unknown_stds_values.columns = myuncertainties
            unknowns_list.append(unknown_stds_values)

    final_standards_list = []
    final_unknowns_list = []
    # concatenates the concentrations and uncertainties dataframes such that there
    # is now one dataframe for each secondary standard that contains both the concentrations
    # and concentrations of the uncertainties for each spot

    for concentration, standard, name in zip(
        concentrations_list, stds_list, secondary_standards
    ):
        df = pd.concat([concentration, standard], axis=1)
        # catches normalized ratio flag from lasertram where bdl was -9999
        df[df < 0] = "b.d.l."
        df.insert(loc=0, column="Spot", value=data.loc[name, "Spot"])

        df.insert(
            loc=1, column="{} wt%".format(oxide), value=stds_data.loc[name, oxide] / 1e4
        )
        df.insert(
            loc=2,
            column="{} 1stdev%".format(oxide),
            value=(
                stds_data.loc[name, "{}_std".format(oxide)]
                / stds_data.loc[name, "{}".format(oxide)]
            )
            * 100,
        )

        final_standards_list.append(df)

    # doing the same thing as above where we make one dataframe for each sample
    # that contains concentrations and uncertainties
    for concentration, sample, name in zip(
        unknown_concentrations_list, unknowns_list, samples_nostandards
    ):
        df = pd.concat([concentration, sample], axis=1)
        df[df < 0] = "b.d.l."
        df.insert(loc=0, column="Spot", value=data.loc[name, "Spot"])

        df.insert(loc=1, column="{} wt%".format(oxide), value=int_std_oxide_array)
        df.insert(loc=2, column="{} 1stdev%".format(oxide), value=unknown_int_std_unc)

        final_unknowns_list.append(df)

    # get final dataframes for secondary standards and unknowns
    df_standards = pd.concat(final_standards_list)
    df_unknowns = pd.concat(final_unknowns_list)

    # all the concentrations and uncertainties
    df_all = pd.concat([df_unknowns, df_standards])
    df_all.reset_index(inplace=True)
    df_all.drop("sample", axis="columns", inplace=True)

    header = "Calculated Concentrations: "

    # placeholder analyte until changed by user
    init_analyte = myanalytes[0]
    
    # calibration standard table data in "Primary Standard" tab
    table_df = calib_std_data.copy()
    table_df.loc["mean"] = table_df.mean()
    table_df.loc["mean", "Spot"] = "average"
    table_df.loc["mean", "bkgd_start":"int_stop"] = np.nan
    table_df.loc["mean", "norm"] = table_df["norm"][0]

    index_as_list = table_df.index.to_list()
    idx = index_as_list.index("mean")
    index_as_list[idx] = calib_std
    table_df.index = index_as_list
    table_df.reset_index(inplace=True)
    columns_as_list = table_df.columns.to_list()
    columns_as_list[0] = "Standard"
    table_df.columns = columns_as_list

    # put it in the table on the right
    final_columns = [{"id": c, "name": c} for c in df_all.columns.to_list()]
    calib_std_columns = [{"id": c, "name": c} for c in columns_as_list]
    return (
        df_all.to_dict("records"),
        final_columns,
        header,
        analyte_list,
        init_analyte,
        calib_std_data.to_json(orient="split"),
        table_df.to_dict("records"),
        calib_std_columns,
    )


@app.callback(
    Output("drift_correct_fig", "figure"),
    [
        Input("analyte_dropdown", "value"),
        Input("stored_calibstd_data", "data"),
        Input("drift_alpha", "value"),
        Input("calculate_btn", "n_clicks"),
    ],
)
def plot_calib_stds(drift_analyte, calib_std_data, alpha, n_clicks):

    if n_clicks < 1:
        raise exceptions.PreventUpdate
    else:
        calib_std_data = pd.read_json(calib_std_data, orient="split")
        norm_analyte = calib_std_data["norm"].unique().tolist()[0]
        if "timestamp" in calib_std_data.columns.tolist():
            # get an array in time units based on timestamp column. This is
            # is in seconds
            x = np.array(
                [np.datetime64(d, "m") for d in calib_std_data["timestamp"]]
            ).astype(np.float64)
        else:
            x = calib_std_data["index"]

        y = calib_std_data[drift_analyte].to_numpy()

        X = sm.add_constant(x)
        # Note the difference in argument order
        model = sm.OLS(y, X).fit()
        # now generate predictions
        ypred = model.predict(X)

        # calc rmse
        RMSE = rmse(y, ypred)

        slope = model.params[1]
        intercept = model.params[0]

        mean = np.mean(y)
        std = np.std(y)
        se = 100 * ((std / mean) / np.sqrt(len(y)))

        # f value stuff
        fvalue = model.fvalue
        f_pvalue = model.f_pvalue
        # alpha is our confidence value. Default would be 99% so it has
        # to be very linear to drift correct
        fcrit = stats.f.ppf(q=1 - alpha, dfn=len(x) - 1, dfd=len(y) - 1)

        # drift correct only if both conditions are true
        if (f_pvalue < alpha) and (fvalue > fcrit):
            drift = "True"
        else:
            drift = "False"

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
        drift_fig.add_hline(
            y=mean,
            line_width=3,
            line_dash="dash",
            line_color="green",
            name="observed mean",
        )

        # line for the linear regression through the points
        drift_fig.add_trace(
            go.Scatter(
                x=np.cumsum(np.diff(x, prepend=x[0])),
                y=ypred,
                mode="lines",
                line=dict(color="black", width=3, dash="dash"),
                name="regression",
            )
        )

        # annotations for the std error of the mean, the RMSE, and whether or not its drift corrected

        drift_fig.add_annotation(x=0, y=mean, text="Mean", showarrow=True, arrowhead=6)
        drift_fig.add_annotation(
            xref="x domain",
            yref="y domain",
            x=0,
            y=1.05,
            text="Std. Err. of mean %: <b><i>{}</i></b>".format(np.round(se, 3)),
            showarrow=False,
        )

        drift_fig.add_annotation(
            xref="x domain",
            yref="y domain",
            x=0.15,
            y=1.05,
            text="Regression stats: <br> RMSE % : <b><i>{}</i></b> <br> p: <b><i>{:E}</i></b>".format(
                np.round(100 * RMSE / mean, 3), np.round(f_pvalue, 3),
            ),
            showarrow=False,
        )

        drift_fig.add_annotation(
            xref="x domain",
            yref="y domain",
            x=0.23,
            y=0.98,
            text="F<sub>val</sub>: <b><i>{}</i></b> <br> F<sub>crit</sub>: <b><i>{}</i></b>".format(
                np.round(fvalue, 3), np.round(fcrit, 3)
            ),
            showarrow=False,
        )

        if drift == "True":

            drift_fig.add_annotation(
                xref="x domain",
                yref="y domain",
                x=0.4,
                y=1.05,
                text="Drift Corrected: <b>{} <br> <i>y = {}x + {}</i></b>".format(
                    drift, np.round(slope, 2), np.round(intercept, 2),
                ),
                showarrow=False,
            )

        else:

            drift_fig.add_annotation(
                xref="x domain",
                yref="y domain",
                x=0.4,
                y=1.05,
                text="Drift Corrected: <b>{} </b>".format(drift,),
                showarrow=False,
            )

        drift_fig.update_layout(
            template="simple_white",
            font=dict(family="Gill Sans", size=20, color=text_color),
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
    app.run_server(debug=True)
