# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import folium
from static_info import df_losses, df_stats, type_list, model_list, status_list, unit_list, date_range, reindex_dates

# %% Initial plots
px.defaults.template = 'plotly_dark'

# Distribution of vehicle losses across types
df_losses_by_type = df_losses.groupby('type').size().reset_index()
# Rename columns to interact with px.pie more easily
df_losses_by_type.columns = ['category', 'Loss count']

fig_losses_pie = px.pie(df_losses_by_type,
                        names='category',
                        values='Loss count',
                        hover_name='category',
                        labels={'category': 'Type'}, 
                        title='Russian vehicle losses by type')
# Add transparent background
fig_losses_pie.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

# Vehicle losses over time
df_losses_grouped_date = df_losses.groupby(['date', 'status']).size()
df_losses_grouped_date = reindex_dates(date_range, df_losses_grouped_date).reset_index()
df_losses_grouped_date.columns = ['Date', 'Status', 'Loss count']

fig_losses_over_time = px.area(df_losses_grouped_date, x='Date', y='Loss count', color='Status')
fig_losses_over_time.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)'
    })

# Map of vehicle losses
ukraine_map = folium.Map(location=[48.379433, 31.16558], zoom_start=6)
ukraine_map.save('map_temp.html')

# %% Create a dash application
dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE, dbc_css])

def create_card_element(element):
    return html.Div(dbc.Card(dbc.CardBody(element)))

# Create an app layout
app.layout = dbc.Container(
    [html.Div([html.H1('Warspotting Russian losses dashboard', style={'textAlign': 'center'}),
               dbc.Card(
                   dbc.CardBody([
                       dbc.Row([
                           dbc.Col(create_card_element([html.H3('Type selection'), dcc.Dropdown(id='type-dropdown', options=type_list, value=type_list[0])]), width=4),
                           dbc.Col(create_card_element([html.H3('Model selection'), dcc.Dropdown(id='model-dropdown', options=model_list[0], value=model_list[0][0], disabled=True)]), width=4),
                           dbc.Col(create_card_element([html.H3('Status selection'), dcc.Dropdown(id='status-dropdown', options=status_list, value=status_list[0])]), width=4)
                            ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col(create_card_element(dcc.Graph(id='losses-pie', figure=fig_losses_pie)), width=6),
                            dbc.Col(create_card_element(dcc.Graph(id='losses-over-time-line', figure=fig_losses_over_time)), width=6)
                            ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col(create_card_element(html.Iframe(id='ukraine-map', srcDoc=open('map_temp.html', 'r').read(), width='100%', height='800')))
                        ])
                        ]), color='dark'
                    )
                ])
    ],
    fluid=True,
    className='dbc')

# %% Callback functions
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

@app.callback(Output('losses-pie', 'figure'),
              Input('type-dropdown', 'value'))
def update_pie_chart(selected_type):
    if selected_type == 'All':
        df_losses_by_type = df_losses.groupby('type').size().reset_index()
        labels = {'category': 'Type'},
        title = 'Russian vehicle losses by type'
    else:
        df_filtered = df_losses[df_losses['type'] == selected_type]
        df_losses_by_type = df_filtered.groupby('model').size().reset_index()
        labels = {'category': 'Model'},
        title = f'Russian {selected_type.lower()} vehicle losses by model'
    
    df_losses_by_type.columns = ['category', 'Loss count']
    # Group small categories (< 1% of total)
    total = df_losses_by_type['Loss count'].sum()
    df_losses_by_type.loc[df_losses_by_type['Loss count'] < 0.01 * total, 'category'] = 'Other'
    df_losses_by_type = df_losses_by_type.groupby('category')['Loss count'].sum().reset_index()

    fig_losses_pie = px.pie(df_losses_by_type,
                        names='category',
                        values='Loss count',
                        hover_name='category',
                        labels=labels,
                        title=title)
    fig_losses_pie.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
    return fig_losses_pie

@app.callback(Output('losses-over-time-line', 'figure'),
              [Input('type-dropdown', 'value'),
               Input('model-dropdown', 'value'),
               Input('status-dropdown', 'value')])
def update_losses_over_time_line(selected_type, selected_model, selected_status):
    if not selected_type == 'All':
        df_filtered = df_losses[df_losses['type'] == selected_type]
        if not selected_model == 'All':
            df_filtered = df_filtered[df_filtered['model'] == selected_model]
    else:
        df_filtered = df_losses
    
    if not selected_status == 'Any':
        df_filtered = df_filtered[df_filtered['status'] == selected_status]

    df_losses_grouped_date = df_filtered.groupby(['date', 'status']).size()
    df_losses_grouped_date = reindex_dates(date_range, df_losses_grouped_date).reset_index()
    df_losses_grouped_date.columns = ['Date', 'Status', 'Loss count']

    fig_losses_over_time = px.area(df_losses_grouped_date,
                                   x='Date',
                                   y='Loss count',
                                   color='Status',
                                   color_discrete_map={
                                       "Abandoned": px.colors.qualitative.Plotly[0],
                                       "Captured": px.colors.qualitative.Plotly[2],
                                       "Damaged": px.colors.qualitative.Plotly[4],
                                       "Destroyed": px.colors.qualitative.Plotly[1]
                                       },
                                   title=f'{selected_type} vehicle losses for {selected_model.lower() if selected_model == "All" else selected_model} model{"s" if selected_model == "All" else ""} over time'
                                   )
    fig_losses_over_time.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)'
    })
    return fig_losses_over_time

# %% Run the app
if __name__ == '__main__':
    app.run_server(debug=True)