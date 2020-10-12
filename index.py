import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import logging
from datetime import datetime
import os
import gc
import psutil

# must add this line in order for the app to be deployed successfully on Heroku
#from app import server
from app import app
# import all pages in the app
from apps import global_situation, singapore, home, keyreport, dyn_graph

# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py



dropdown = dbc.DropdownMenu(

    children=[
        dbc.DropdownMenuItem("Home", href="/home"),
        dbc.DropdownMenuItem("Dynamic Graphs", href="/dyn_graph"),
        dbc.DropdownMenuItem("BO PI Dashboard", href="/keyreport?id=1"),
        dbc.DropdownMenuItem("NS BH Report", href="/keyreport?id=2"),
    ],
    nav = True,
    in_navbar = True,
    label = "Explore",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/Ericsson_logo.png", height="70px")),
                        dbc.Col(dbc.NavbarBrand("DGS-One Dashboard", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')]
              )
def display_page(pathname):
    if pathname == '/keyreport':
        return keyreport.layout
    #elif pathname == '/global_situation':
    #    return global_situation.layout
    elif pathname == '/dyn_graph':
        return dyn_graph.layout
    elif pathname == '/singapore':
        return singapore.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)