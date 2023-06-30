from dash import Dash, dcc, html, Input, Output, callback
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
import pandas as pd
from packages.geo import geoM
from packages.General_statistics import generalStatistics
from packages.data_prep import GetData
import os
from datetime import datetime, timedelta

##  data preparation 



username , password = GetData.authentication()
data_analysis , data_read_run = GetData.main (username , password)

#data_analysis = pd.read_csv('packages/data/dcc_schubert_ENA_Search_analysis.csv')
#data_analysis = data_analysis.fillna('-1')
#data_read_run = pd.read_csv('packages/data/dcc_schubert_ENA_Search_read_run.csv',low_memory=False)
#data_read_run = data_read_run.fillna('-1')

#### header
def header():
   
   res = html.Div([
        html.H1(children=[html.Strong("Data Hub Dashboard")]),
         html.H3(children='---[ {} ]---'.format(username)),
          html.P(children=[html.Em("This dashboard presents information related to your data hub." )]),
   ] ,  className="header-container",
   style ={'width':'100%', 'text-align':'center', 'background-color': '#18974C', 'padding-top': '2%','padding-botton':'2%','display': 'flex','flex-direction': 'column'}
   )

   return res

####
def statistics ():
    stats_r = {}
    stats_a = {}
    # run statistics 
    stats_r['Total raw sequence datasets'] = len(data_read_run)
    stats_r['Total sequencing platforms'] = data_read_run['instrument_platform'].nunique()
    stats_r['Total sequencing platform models'] = data_read_run['instrument_model'].nunique()
    stats_r['Data Providers (Collaborators)'] = data_read_run['center_name'].nunique()

    # analysis statistics
    stats_a['Total analyses'] =  len(data_analysis)
    stats_a['Analysis pipelines'] = data_analysis['pipeline_name'].nunique()

    res =html.Div(
        html.Div([
        dbc.Row(
        [
                dbc.Col(
                    [
                        html.H2(value),
                        html.P(key)
                    ],
                    width=3
                )
                for key, value in stats_r.items()
            ],
            style={'width':'50%','margin-left':'25%','text-align':'center'}
        ),
        dbc.Row(
        [
                dbc.Col(
                    [
                        html.H2(value),
                        html.P(key)
                    ],
                    width=6
                )
                for key, value in stats_a.items()
            ],
            style={'width':'25%','margin-left':'38%','text-align':'center'}
        )
        
        ],
        ),
        style={'width':'100%','background-color':'#D0D0CE'}
    )



    return html.Div(res)


### plot 
def map () : 
    data_map = geoM.df_map(list(data_read_run['country']))
    fig1 = geoM.Choropleth_map(data_map)
    #fig1.update_layout(height=2000)
    fig = html.Div([dcc.Graph(figure=fig1)])
    return fig

##### instrument platform

def platfrom ():
    fig = generalStatistics.piePlatform(list(data_read_run['instrument_platform']))
    fig = html.Div([html.P('Data hub holdings composition: Instrument Platform'),
        dcc.Graph(figure=fig)],
        style={
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'center',
            'flex-direction': 'column',
        }
        )
    return fig

#####  evolution of submissions
def submissionsEvo():
    fig1 , fig2= generalStatistics.submissionsEvo(data_read_run,data_analysis,username)
    return html.Div([
                    dbc.Row([
                        dbc.Col([dcc.Graph(figure=fig1),], width=6),
                        dbc.Col([dcc.Graph(figure=fig2),], width=6)
                    ])
                     ])

############### Body

body = html.Div([
    html.Div([
        header(),
        statistics(),
        html.Hr(),
        html.Div([
            dbc.Row([
            dbc.Col([map(),], width=8),
            dbc.Col([platfrom(),], width=4)
            ]),
            submissionsEvo(),
        ],
            style={'width' : '80%','margin-left':'10%','text-align':'center'}
        )

    ])
])


########## app

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    #'static/main.css'
]
app = DjangoDash('ena_datahub_dashboard', external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True,
                )
app.layout = html.Div(
        children=[
            body, 
            html.Br(),
            html.Br(),
            html.Br(),

        ], 
        style= {'width' : '100%'}
    )