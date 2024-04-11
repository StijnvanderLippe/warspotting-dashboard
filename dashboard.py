# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import os
from static_info import df_losses, df_stats, type_list, model_list, status_list, unit_list

# Initial plots
px.defaults.template = 'plotly_dark'

fig_stats_pie = px.pie(df_stats, names='type_name', values='counts.losses', title='Russian losses by vehicle type')
# Add transparent background
fig_stats_pie.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

# Create a dash application
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])

# Create an app layout
app.layout = dbc.Container(
    [html.Div([html.H1('Warspotting Russian losses dashboard', style={'textAlign': 'center'}),
               html.Div(dcc.Graph(id='stats-pie', figure=fig_stats_pie)),
               html.Div([html.H3('Type selection'), dcc.Dropdown(id='type-dropdown', options=type_list, value=type_list[0]), html.Br(),
                         html.H3('Model selection'), dcc.Dropdown(id='model-dropdown', options=model_list[0], value=model_list[0][0], disabled=True)])
                ])
    ],
    fluid=True,
    className='dbc')


@app.callback([Output('model-dropdown', 'options'),
               Output('model-dropdown', 'disabled')],
              Input('type-dropdown', 'value'))
def set_model_options(selected_type):
    if selected_type == 'All':
        model_options = model_list[0]
        disabled = True
    else:
        model_options = model_list[type_list.index(selected_type)]
        disabled = False
    return model_options, disabled

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)