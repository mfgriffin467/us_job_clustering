import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from textwrap import dedent as d
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
time_window = 50
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Read data and create 

df_final = pd.read_csv("results.csv")

app.layout = html.Div([
    html.H1(children='JOBS DASHBOARD'),

    html.Div([
    	html.Label(children='Job family'),
        dcc.Dropdown(
		    id='job',
            options=[{'label': i, 'value': i} for i in df_final['Job Family'].unique()],
            value='Management'
            ),
        html.Br(),
        html.Label(children='Chart scaling'),
        dcc.RadioItems(
            id='yaxis-type',
            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            value='Linear',
            labelStyle={'display': 'inline-block'}
            )
        ]),

    html.Div([
        dcc.Graph(id='graphic1')
        ]),

    html.Div([
        dcc.Graph(id='graphic2')
        ]),



    html.Div([
        dcc.Markdown(d('''
        ### APPROACH

        - Analysis is for illustrative purposes only - this should not be used for any decision-making

        ''')),
    ]),

], style={'columnCount': 2})


@app.callback(
	Output('graphic1', 'figure'),
    [Input('job', 'value'),
    Input('yaxis-type', 'value')])


def update_cases(job, yaxis_type):
	return {
            'data': [dict(
            	x=df_final[df_final['Job Family'] == job]['a_mean'],
            	y=df_final[df_final['Job Family'] == job]['GP_pred_1'],
                text=df_final[df_final['Job Family'] == job]['Title'],
            	mode='markers',
            	opacity=0.7,
            	marker={
            		'size': 10,
                    'color': 'orange',
            		'line': {'width': 0.5, 'color': 'white'}
                    },
                )
            ],
            'layout': dict(
                title="Covid cases",
                xaxis={'title': 'time'},
                yaxis={
                    'title': 'count',
                    'type': 'linear' if yaxis_type == 'Linear' else 'log'
                    },
                margin={'l': 100, 'b': 40, 't': 100, 'r': 10},
                hovermode='closest'
            )
        }



@app.callback(
	Output('graphic2', 'figure'),
    [Input('job', 'value'),
    Input('yaxis-type', 'value')])


def update_cases_v2(job, yaxis_type):
	return {
            'data': [dict(
            	x=df_final[df_final['Job Family'] == job]['GP_pred_1'],
            	y=df_final[df_final['Job Family'] == job]['tot_emp'],
                text=df_final[df_final['Job Family'] == job]['Title'],
            	mode='markers',
            	opacity=0.7,
            	marker={
            		'size': 10,
                    'color': 'orange',
            		'line': {'width': 0.5, 'color': 'white'}
                    },
                )
            ],
            'layout': dict(
                title="Covid cases",
                xaxis={'title': 'time'},
                yaxis={
                    'title': 'count',
                    'type': 'linear' if yaxis_type == 'Linear' else 'log'
                    },
                margin={'l': 100, 'b': 40, 't': 100, 'r': 10},
                hovermode='closest'
            )
        }



if __name__ == '__main__':
    app.run_server(debug=True)