import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import networkx as nx
from network_stack import *
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

obj=GraphStack()
graph=obj.make_graph()
pos=obj.position_of_nodes(graph)
node_x,node_y,edge_x,edge_y=obj.get_coordinate(pos,graph)
node_color,node_text=obj.get_color_text()

app.layout = html.Div([
    html.Div([html.H1("Stack-Overflow  Tag Graph")], className="row", style={'textAlign': "center"}),
    html.Div([dcc.Graph(id="stack-graph")]),
    html.Div([html.Span("Slide to change Size of nodes", style={"text-align": "center", 'padding': 10}, className="row"),
              dcc.Slider(id="nodesSize", min=10, max=30, value=10, step=2, updatemode="drag",
                         marks={10: "10", 20: "20", 30: "30"}, className="row")],
             style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "40%", "padding": 20})
], className="container")


@app.callback(
    dash.dependencies.Output("stack-graph", "figure"),
    [dash.dependencies.Input("nodesSize", "value")])
def update_graph(n):
    edge_trace = go.Scatter(x=edge_x, y=edge_y,
                            line=dict(width=0.5, color='#888'),
                            hoverinfo='none',
                            mode='lines')

    node_trace = go.Scatter(
                            x=node_x, y=node_y,
                             mode='markers',
                            hoverinfo='text',
                            marker=dict(showscale=False,
                                        colorscale='Jet',
                                        color=[],
                                        size=n,
                                        ))

    
    node_trace.marker.color = node_color
    node_trace.text = node_text

    figure = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(title='Stack Overflow Tag Network',
                                        
                                        showlegend=False,
                                        hovermode='closest',
                                        margin=dict(b=20,l=5,r=5,t=40),
                                        annotations=[ dict(text="Author: Vishal Dhiman",
                                                            showarrow=False,
                                                            xref="paper", yref="paper",
                                                            x=0.005, y=-0.002 ) ],
                                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    



    return figure

if __name__ == '__main__':
    app.run_server(debug=True)