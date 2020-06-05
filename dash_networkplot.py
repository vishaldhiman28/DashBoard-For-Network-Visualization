import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import networkx as nx
from network_stack import *
import plotly.graph_objs as go
import dash_table
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = app.server


obj=GraphStack()
links_data=obj.get_links_data()
nodes_data=obj.get_nodes_data()
graph=obj.make_graph()
span_graph=obj.span_tree(graph)
group_visual=obj.group_visual()

colors = {
    'background': '#ff4d2e',
    'text': '#7FDBFF'
}
data_options=['Nodes Dataset','Links Dataset']
def generate_table1(max_rows=10):
    
    return html.Table(

            # Header
            
            [html.Tr([html.Th(col) for col in links_data.columns])] +

            # Body
            [html.Tr([
                html.Td(links_data.iloc[i][col]) for col in links_data.columns
            ]) for i in range(min(len(links_data), 10))]
            )

def generate_table2():
    return html.Table(
            # Header
            [html.Tr([html.Th(col) for col in nodes_data.columns])] +

            # Body
            [html.Tr([
                html.Td(nodes_data.iloc[i][col]) for col in nodes_data.columns
            ]) for i in range(min(len(links_data), 10))]
            )

network_options=['Main Network','Minimum Spannining Tree']


app.layout = html.Div([
    html.Div([html.H1("Network Visualization")], className="row", style={'textAlign': "center"}),
    html.Div([html.H3('Dataset Info')], className="row", style={'textAlign': "center"}),
    html.Div([html.H4("This dataset is a result of a Developer's search activity on Stack-Overflow for a particular problem \
    related to development based on Programming Language.    ")], 
    className="row", style={'textAlign': "center"}),
    html.Div([html.H4('Nodes Dataset')], className="row", style={'textAlign': "center"}),
    dash_table.DataTable(
        id='datatable1',
        columns=[
            {"name": i, "id": i} for i in nodes_data.columns
        ],
        data=nodes_data.to_dict('records'),
        selected_columns=[],
        style_header={
        'backgroundColor': '#ff4d2e',
        'fontWeight': 'bold'
        },
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
    ),
    html.Div([html.H1("")], className="row", style={'textAlign': "center"}),
    html.Div([html.H4('Links Dataset')], className="row", style={'textAlign': "center"}),
    dash_table.DataTable(
        id='datatable2',
        columns=[
            {"name": i, "id": i} for i in links_data.columns
        ],
        data=links_data.to_dict('records'),
        selected_columns=[],
        style_header={
        'backgroundColor': '#ff4d2e',
        'fontWeight': 'bold'
        },
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
    ),
    html.Div([html.H1("")], className="row", style={'textAlign': "center"}),
    
    html.Div([html.H1("Stack-Overflow Tag Graph")], className="row", style={'textAlign': "center"}),
    html.Div([html.Span("", style={"text-align": "center"}, className="row"),dcc.RadioItems(
        id='network-opt',
        options=[{'label': k, 'value': k} for k in network_options],
        value='Main Network')],
         style={"display": "block","margin-left": "auto", "margin-right": "auto", "width": "40%", "padding": 20}),
    html.Div([dcc.Graph(id="stack-graph")]),
    html.Div([html.H1("")], className="row", style={'textAlign': "center"}),
    html.Div([html.H1("Choose group to see Data group-wise")], className="row", style={'textAlign': "center"}),
    html.Div([html.H1("")], className="row", style={'textAlign': "center"}),
    html.Div([html.Span("", style={"text-align": "center"}, className="row"),dcc.Dropdown(
        id="group-opt",
        options=[
            {'label': key, 'value': key} for key in group_visual.keys()],
        value=1),],
         style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "40%", "padding": 20}),
    html.Div([dcc.Graph(id="group-graph")],style={"vertical-align": "center"}),
    html.Div([html.A('Developer: Vishal Dhiman', href='',target="_blank")],className="row", style={'textAlign': "center"}),
    html.Div([html.A("Github", href='https://github.com/vishaldhiman28/', target="_blank")],className="row", style={'textAlign': "center"}),
    html.Div([html.A("LinkedIn", href='https://www.linkedin.com/in/vishaldhiman28/', target="_blank")],className="row", style={'textAlign': "center"}),
    ], className="container")


@app.callback(
    dash.dependencies.Output("group-graph", "figure"),
    [dash.dependencies.Input("group-opt", "value")])
def update_group_graph(opt_g):
    p_graph=obj.make_group_graph(opt_g,graph)
    pos=obj.position_of_nodes(p_graph)
    node_x,node_y,edge_x,edge_y=obj.get_coordinate(pos,p_graph,"Main Network")

    edge_trace = go.Scatter(x=edge_x, y=edge_y,
                            line=dict(width=0.8),
                            hoverinfo='none',
                            mode='lines')

    node_trace = go.Scatter(
                            x=node_x, y=node_y,
                            mode='markers+text',
                            name='Markers and text',
                            text=[],
                            marker=dict(showscale=False,
                            size=[]
                            ))
    node_trace.text = list(pos.keys())
    node_trace.marker.size = [20 for i in range(len(pos.keys()))]
    figure = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(title='',
                                       width=1000,
                                       height=500,
                                        
                                        showlegend=False,
                                        hovermode='closest',
                                        margin=dict(b=20,l=5,r=5,t=40),
                                        annotations=[ dict(text="",
                                                            showarrow=False,
                                                            xref="paper", yref="paper",
                                                            x=0.005, y=-0.002 ) ],
                                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    return figure



@app.callback(
    dash.dependencies.Output("stack-graph", "figure"),
    [dash.dependencies.Input("network-opt", "value")])
def update_graph(opt):
    if opt=="Main Network":
        pos=obj.position_of_nodes(graph)
        node_x,node_y,edge_x,edge_y=obj.get_coordinate(pos,graph,opt)
        node_color,text,size,hover_text=obj.get_color_text(graph)

    elif opt=="Minimum Spannining Tree":
        pos=obj.position_of_nodes(span_graph)
        node_x,node_y,edge_x,edge_y=obj.get_coordinate(pos,span_graph,opt)
        node_color,text,size,hover_text=obj.get_color_text(span_graph)
        

    
    
    edge_trace = go.Scatter(x=edge_x, y=edge_y,
                            line=dict(width=0.8),
                            hoverinfo='none',
                            mode='lines')

    node_trace = go.Scatter(
                            x=node_x, y=node_y,
                            mode='markers+text',
                            hoverinfo='text',
                            hovertext=[],
                            name='Markers and Text',
                            text=[],
                            opacity=1,
                            marker=dict(showscale=False,
                                        colorscale='YlGnBu',
                                        color=[],
                                        size=[],
                                        ))

    
    node_trace.marker.color = node_color
    node_trace.text = text
    node_trace.marker.size = size
    node_trace.hovertext=hover_text
    figure = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(title='',
                                       width=1100,
                                       height=1100,
                                        
                                        showlegend=False,
                                        hovermode='closest',
                                        margin=dict(b=20,l=5,r=5,t=40),
                                        annotations=[ dict(text="",
                                                            showarrow=False,
                                                            xref="paper", yref="paper",
                                                            x=0.005, y=-0.002 ) ],
                                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    return figure





if __name__ == '__main__':
    app.run_server(debug=True)
