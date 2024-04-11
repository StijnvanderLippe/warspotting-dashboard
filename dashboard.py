# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import os
from static_info import df_losses, df_stats, type_list, model_list, status_list, unit_list, date_range, reindex_dates

# Initial plots
px.defaults.template = 'plotly_dark'

# Distribution of vehicle losses across types
fig_stats_pie = px.pie(df_stats, names='type_name', values='counts.losses', title='Russian losses by vehicle type')
# Add transparent background
fig_stats_pie.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

# Vehicle losses over time
df_losses_grouped_date = df_losses.groupby('date').size()
df_losses_grouped_date = reindex_dates(date_range, df_losses_grouped_date)

fig_losses_over_time = px.line(df_losses_grouped_date, title='Vehicle losses over time')
fig_losses_over_time.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'showlegend': False
    })

# Create a dash application
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])

# Create an app layout
app.layout = dbc.Container(
    [html.Div([html.H1('Warspotting Russian losses dashboard', style={'textAlign': 'center'}),
               dbc.Card(
                   dbc.CardBody([
                       dbc.Row([
                           dcc.Graph(id='stats-pie', figure=fig_stats_pie)
                           ]),
                       html.Br(),
                       dbc.Row([
                           dbc.Col([html.H3('Type selection'), dcc.Dropdown(id='type-dropdown', options=type_list, value=type_list[0])], width=6),
                           dbc.Col([html.H3('Model selection'), dcc.Dropdown(id='model-dropdown', options=model_list[0], value=model_list[0][0], disabled=True)], width=6)
                            ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([dcc.Graph(id='losses-over-time-line', figure=fig_losses_over_time)])
                            ])
                        ])
                    )
                ])
    ],
    fluid=True,
    className='dbc')


@app.callback([Output('model-dropdown', 'options'),
               Output('model-dropdown', 'value'),
               Output('model-dropdown', 'disabled')],
              Input('type-dropdown', 'value'))
def set_model_options(selected_type):
    if selected_type == 'All':
        model_options = model_list[0]
        model_value = model_options[0]
        disabled = True
    else:
        model_options = model_list[type_list.index(selected_type)]
        model_value = model_options[0]
        disabled = False
    return model_options, model_value, disabled

@app.callback(Output('losses-over-time-line', 'figure'),
              [Input('type-dropdown', 'value'),
               Input('model-dropdown', 'value')])
def update_losses_over_time_line(selected_type, selected_model):
    if not selected_type == 'All':
        filtered_df = df_losses[df_losses['type'] == selected_type]
        if not selected_model == 'All':
            filtered_df = filtered_df[filtered_df['model'] == selected_model]
    else:
        filtered_df = df_losses
    df_losses_grouped_date = filtered_df.groupby('date').size()
    df_losses_grouped_date = reindex_dates(date_range, df_losses_grouped_date)

    fig_losses_over_time = px.line(df_losses_grouped_date, 
                                   title=f'{selected_type} vehicle losses for {selected_model.lower() if selected_model == "All" else selected_model} model{"s" if selected_model == "All" else ""} over time',
                                   labels={'index': 'Date', 'value': 'Loss count'})
    fig_losses_over_time.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'showlegend': False
    })
    return fig_losses_over_time

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)