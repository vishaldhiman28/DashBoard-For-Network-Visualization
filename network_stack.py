# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import networkx as nx


class GraphStack():
  #reading files
  def __init__(self):

    self.stack_network_links=pd.read_csv("stack_network_links.csv") 
    self.stack_network_nodes=pd.read_csv("stack_network_nodes.csv")

  def make_graph(self):
    
    graph=nx.Graph()
    #adding nodes
    for row in range(self.stack_network_nodes.shape[0]):
      graph.add_node(self.stack_network_nodes.iloc[row]["name"],group=self.stack_network_nodes.iloc[row]["group"],nodesize=self.stack_network_nodes.iloc[row]["nodesize"])
    
    #adding eges  
    for row in range(self.stack_network_links.shape[0]):
      graph.add_edge(self.stack_network_links.iloc[row]["source"],self.stack_network_links.iloc[row]["target"],weight=self.stack_network_links.iloc[row]["value"])
    return graph 

  def position_of_nodes(self,graph):
    #defines coordinate of nodes 
    pos = nx.drawing.spring_layout(graph,k=0.70,iterations=60)
    return pos

  def get_coordinate(self,pos,graph):
    node_x=[]
    node_y=[]
    
    #getting x_corrdinate and y_coordinates of nodes in list
    for key in sorted(pos.keys()):
      node_x.append(pos[key][0])
      node_y.append(pos[key][1])
      
    edge_x=[]
    edge_y=[]

    #getting start-end coordinated of nodes in the list
    for edge in sorted(graph.edges()):
      edge_x.append(pos[edge[0]][0])
      edge_y.append(pos[edge[0]][1])
      edge_x.append(pos[edge[1]][0])
      edge_y.append(pos[edge[1]][1])
     
    return node_x,node_y,edge_x,edge_y

  def get_color_text(self):
    #setting color and text of each node 
    node_color=[]
    node_text=[]
    d=self.stack_network_nodes.sort_values('name')
    for _ , r in d.iterrows():
      node_color.append(r['group'])
      t= "Tag Name: "+r['name']+ "\n.Tag Group: "+str(r['group'])
      node_text.append(t)
     
    return node_color,node_text

